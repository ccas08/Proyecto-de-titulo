
from wsgiref.validate import validator
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import get_user_model


# for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {"password": forms.PasswordInput()}


# for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model =  get_user_model()
        fields = ["first_name", "last_name", "username", "password"]
        
        widgets = {"password": forms.PasswordInput()}
        

class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ["email", "status", "profile_pic"]


# for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "password"]
        widgets = {"password": forms.PasswordInput()}


class PatientForm(forms.ModelForm):
    # this is the extrafield for linking patient and their assigend doctor
    # this will show dropdown __str__ method doctor model is shown on html so override it
    # to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId = forms.ModelChoiceField(
        queryset=models.Doctor.objects.all().filter(status=True),
        empty_label="Nombre del doctor",
        to_field_name="user_id",
    )

    class Meta:
        model = models.Patient
        fields = ["status", "Type", "profile_pic", "email"]

