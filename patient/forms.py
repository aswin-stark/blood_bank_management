from django import forms
from django.contrib.auth.models import User
from . import models
from blood.forms import validate_password_rules


class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password_rules])
    email = forms.EmailField(required=True, label='Email address')

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    
    class Meta:
        model=models.Patient
        fields=['age','bloodgroup','disease','address','doctorname','mobile','profile_pic']
