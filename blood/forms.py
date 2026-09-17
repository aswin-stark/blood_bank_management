from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from . import models


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class BloodGivingForm(forms.ModelForm):
    class Meta:
        model=models.BloodGiving
        fields=['bloodgroup','unit','source','details']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']


class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise ValidationError('No account was found with this username.')
        return username

    def clean_new_password(self):
        password = self.cleaned_data['new_password']
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one letter.')
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError('Password must contain at least one symbol.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') and cleaned_data.get('confirm_password'):
            if cleaned_data['new_password'] != cleaned_data['confirm_password']:
                raise ValidationError('The passwords do not match.')
        return cleaned_data


def validate_password_rules(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError('Password must contain at least one letter.')
    if not re.search(r'[^A-Za-z0-9]', password):
        raise ValidationError('Password must contain at least one symbol.')
