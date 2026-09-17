from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum,Q
from django.db import transaction
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import logging
from donor import models as dmodels
from patient import models as pmodels
from donor import forms as dforms
from patient import forms as pforms

logger = logging.getLogger(__name__)

def _send_account_notification(user, subject, message, approval_type, blood_group, units, notification_status):
    if not user.email:
        return False, 'The recipient profile has no email address. Add an email address to that patient or donor account first.'
    if not all((settings.EMAILJS_SERVICE_ID, settings.EMAILJS_TEMPLATE_ID, settings.EMAILJS_PUBLIC_KEY)):
        return False, 'EmailJS service ID, template ID, or public key is missing.'
    try:
        payload = {
            'service_id': settings.EMAILJS_SERVICE_ID,
            'template_id': settings.EMAILJS_TEMPLATE_ID,
            'user_id': settings.EMAILJS_PUBLIC_KEY,
            'template_params': {
                'to_email': user.email,
                'to_name': user.get_full_name() or user.username,
                'subject': subject,
                'message': message,
                'approval_type': approval_type,
                'notification_status': notification_status,
                'is_approved': notification_status == 'Approved',
                'blood_group': blood_group,
                'units': units,
                # Configure the EmailJS template's Reply-To field as {{reply_to}}.
                'reply_to': settings.EMAILJS_REPLY_TO_EMAIL,
            },
        }
        if settings.EMAILJS_PRIVATE_KEY:
            payload['accessToken'] = settings.EMAILJS_PRIVATE_KEY
        request = Request(
            settings.EMAILJS_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            },
            method='POST',
        )
        with urlopen(request, timeout=10) as response:
            if 200 <= response.status < 300:
                return True, ''
            return False, 'EmailJS returned HTTP {0}.'.format(response.status)
    except HTTPError as error:
        error_detail = error.read().decode('utf-8', errors='replace')
        logger.error('EmailJS rejected the notification (HTTP %s): %s', error.code, error_detail)
        return False, 'EmailJS returned HTTP {0}: {1}'.format(error.code, error_detail)
    except (URLError, OSError, ValueError) as error:
        logger.error('EmailJS notification could not be sent: %s', error)
        return False, 'EmailJS connection error: {0}'.format(error)

def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def forgot_password_view(request):
    password_form = forms.PasswordResetForm()
    if request.method == 'POST':
        password_form = forms.PasswordResetForm(request.POST)
        if password_form.is_valid():
            user = User.objects.get(username=password_form.cleaned_data['username'])
            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            return render(request, 'blood/forgot_password.html', {'password_form': forms.PasswordResetForm(), 'reset_complete': True})
    return render(request, 'blood/forgot_password.html', {'password_form': password_form})

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def afterlogin_view(request):
    if is_donor(request.user):      
        return redirect('donor/donor-dashboard')
                
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        return redirect('admin-dashboard')

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict={

        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    dict={
        'bloodForm':forms.BloodGivingForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodGivingForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            with transaction.atomic():
                stock=models.Stock.objects.get(bloodgroup=bloodgroup)
                stock.unit=bloodForm.cleaned_data['unit']
                stock.save()
                bloodForm.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)

@login_required(login_url='adminlogin')
def admin_giving_view(request):
    giving=models.BloodGiving.objects.all().order_by('-date')
    return render(request,'blood/admin_giving.html',{'giving':giving})


@login_required(login_url='adminlogin')
def admin_donor_view(request):
    donors=dmodels.Donor.objects.all()
    return render(request,'blood/admin_donor.html',{'donors':donors})

@login_required(login_url='adminlogin')
def donor_detail_view(request,pk):
    donor=get_object_or_404(dmodels.Donor,pk=pk)
    donations=dmodels.BloodDonate.objects.filter(donor=donor).order_by('-date')
    requests=models.BloodRequest.objects.filter(request_by_donor=donor).order_by('-date')
    return render(request,'blood/profile_detail.html',{'profile':donor,'profile_type':'Donor','donations':donations,'requests':requests})

@user_passes_test(lambda user: user.is_staff, login_url='adminlogin')
def toggle_donor_status_view(request,pk):
    donor=get_object_or_404(dmodels.Donor,pk=pk)
    if request.method == 'POST':
        donor.user.is_active=not donor.user.is_active
        donor.user.save(update_fields=['is_active'])
    return redirect('donor-detail',pk=donor.pk)

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    patients=pmodels.Patient.objects.all()
    return render(request,'blood/admin_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
def patient_detail_view(request,pk):
    patient=get_object_or_404(pmodels.Patient,pk=pk)
    requests=models.BloodRequest.objects.filter(request_by_patient=patient).order_by('-date')
    received=requests.filter(status='Approved')
    return render(request,'blood/profile_detail.html',{'profile':patient,'profile_type':'Patient','requests':requests,'received':received})

@user_passes_test(lambda user: user.is_staff, login_url='adminlogin')
def toggle_patient_status_view(request,pk):
    patient=get_object_or_404(pmodels.Patient,pk=pk)
    if request.method == 'POST':
        patient.user.is_active=not patient.user.is_active
        patient.user.save(update_fields=['is_active'])
    return redirect('patient-detail',pk=patient.pk)


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=pforms.PatientUserForm(request.POST,instance=user)
        patientForm=pforms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    requests=models.BloodRequest.objects.all().filter(status='Pending').order_by('-date')
    stock_by_group={stock.bloodgroup: stock.unit for stock in models.Stock.objects.all()}
    for request_item in requests:
        request_item.available_units=stock_by_group.get(request_item.bloodgroup, 0)
    return render(request,'blood/admin_request.html',{'requests':requests,'active_tab':'requests'})

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    requests=models.BloodRequest.objects.all().exclude(status='Pending').order_by('-date')
    return render(request,'blood/admin_request_history.html',{'requests':requests,'active_tab':'history'})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    donations=dmodels.BloodDonate.objects.filter(status='Pending').order_by('-date')
    return render(request,'blood/admin_donation.html',{'donations':donations,'active_tab':'requests'})

@login_required(login_url='adminlogin')
def admin_donation_history_view(request):
    donations=dmodels.BloodDonate.objects.exclude(status='Pending').order_by('-date')
    return render(request,'blood/admin_donation_history.html',{'donations':donations,'active_tab':'history'})

@login_required(login_url='adminlogin')
def update_approve_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    approved=False
    with transaction.atomic():
        stock=models.Stock.objects.select_for_update().get(bloodgroup=bloodgroup)
        if stock.unit >= unit:
            stock.unit=stock.unit-unit
            stock.save()
            req.status="Approved"
            req.save()
            approved=True
        else:
            message="Out of stock: only "+str(stock.unit)+" unit(s) of "+bloodgroup+" available, but "+str(unit)+" requested."

    if approved:
        request_user = (req.request_by_patient.user if req.request_by_patient_id else req.request_by_donor.user)
        email_sent, email_error = _send_account_notification(
            request_user,
            'Blood request approved',
            'Your blood request for {0} ({1} unit(s)) has been approved. Please log in to view the updated request history.'.format(bloodgroup, unit),
            'Blood request',
            bloodgroup,
            unit,
            'Approved',
        )
        if email_sent:
            messages.success(request, 'Request approved and confirmation email sent.')
        else:
            messages.warning(request, 'Request approved, but the email could not be sent. {0}'.format(email_error))

    requests=models.BloodRequest.objects.all().filter(status='Pending').order_by('-date')
    stock_by_group={stock.bloodgroup: stock.unit for stock in models.Stock.objects.all()}
    for request_item in requests:
        request_item.available_units=stock_by_group.get(request_item.bloodgroup, 0)
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message,'active_tab':'requests'})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    request_user = (req.request_by_patient.user if req.request_by_patient_id else req.request_by_donor.user)
    email_sent, email_error = _send_account_notification(
        request_user,
        'Blood request not approved',
        'Your blood request for {0} ({1} unit(s)) was not approved. Please contact the blood bank if you need further assistance.'.format(req.bloodgroup, req.unit),
        'Blood request',
        req.bloodgroup,
        req.unit,
        'Not approved',
    )
    if email_sent:
        messages.success(request, 'Request rejected and notification email sent.')
    else:
        messages.warning(request, 'Request rejected, but the email could not be sent. {0}'.format(email_error))
    return HttpResponseRedirect('/admin-request')

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()

    donation.status='Approved'
    donation.save()
    email_sent, email_error = _send_account_notification(
        donation.donor.user,
        'Donation approved',
        'Your donation of {0} unit(s) of {1} has been approved and added to the blood stock.'.format(donation_blood_unit, donation_blood_group),
        'Blood donation',
        donation_blood_group,
        donation_blood_unit,
        'Approved',
    )
    if email_sent:
        messages.success(request, 'Donation approved and confirmation email sent.')
    else:
        messages.warning(request, 'Donation approved, but the email could not be sent. {0}'.format(email_error))
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    email_sent, email_error = _send_account_notification(
        donation.donor.user,
        'Donation not approved',
        'Your donation of {0} unit(s) of {1} was not approved. Please contact the blood bank if you need further assistance.'.format(donation.unit, donation.bloodgroup),
        'Blood donation',
        donation.bloodgroup,
        donation.unit,
        'Not approved',
    )
    if email_sent:
        messages.success(request, 'Donation rejected and notification email sent.')
    else:
        messages.warning(request, 'Donation rejected, but the email could not be sent. {0}'.format(email_error))
    return HttpResponseRedirect('/admin-donation')
