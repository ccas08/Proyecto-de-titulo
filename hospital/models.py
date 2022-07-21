
from optparse import Values
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.core import validators
from django.core.exceptions import ValidationError
import sys
from itertools import cycle
import re


from django.contrib.auth.models import AbstractUser

def validarLetras(value):
    for i in value:
        if not i.isalpha():
            print("aqui")
            raise ValidationError("Este campo solo acepta letras") 

def validarRut(value):   
    if not re.compile("^(\d{1,3}(?:\.\d{1,3}){2}-[\dkK])$").match(value):
        raise ValidationError("Formato incorrecto del Rut, recuerde: \n xx.xxx.xxx.-x") 

def validarContraseña(value):   
    if not re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$").match(value):
        raise ValidationError("La contraseña debe contener al menos : Mayúsculas, minúsculas , números, carácteres especiales") 

def validarEmail(value):   
    print("aqui")
    if not re.compile("(?:[a-z0-9!#$%&*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])").match(value):
        raise ValidationError("Formato incorrecto del Correo Electrónico, recuerde:\n ejemplo@email.com ") 
    
def validarOpcion(value):
    if re.compile("Elegir tipo de diabetes").match(value):
        raise ValidationError("Por favor elegir una opción correcta para el campo") 

        

        
        
class User(AbstractUser):
    username= models.CharField(max_length=20, validators=[validarRut],unique=True)
    first_name= models.CharField(max_length=20, validators=[validarLetras])
    last_name = models.CharField(max_length=20, validators=[validarLetras])
    password=models.CharField(max_length=20, validators=[validarContraseña],unique=True)

    #REQUIRED_FIELDS = ["first_name", "last_name"]
    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/"
    )
    email = models.CharField(max_length=60, validators=[validarEmail] )
    status = models.BooleanField(default=False)

   
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "({})".format(self.user.first_name + " " + self.user.last_name)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/PatientProfilePic/", blank=True
    )
    email = models.CharField(max_length=60, validators=[validarEmail])
    MY_CHOICES = (
        ('Elegir tipo de diabetes', 'Elegir tipo de diabetes'),
        ('Diabetes tipo 1', 'Diabetes tipo 1'),
        ('Diabetes tipo 2', 'Diabetes tipo 2'),
        ('Diabetes gestacional', 'Diabetes gestacional'),

    )
    Type = models.CharField(max_length=100, null=False, choices=MY_CHOICES, validators=[validarOpcion], default=MY_CHOICES[0])
    assignedDoctorId = models.PositiveIntegerField(null=True)
    status = models.BooleanField(default=False)
    libreview_email= models.CharField(max_length=60)
    libreview_password = models.CharField(max_length=20)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.Type + ")"


class PatientReport(models.Model):
    patientId = models.PositiveIntegerField(null=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    patientName = models.CharField(max_length=40)
    email = models.CharField(max_length=60)
    Type = models.CharField(max_length=100, null=True)
    reportGenerado= models.CharField(max_length=20, null=True)
    Gmi = models.FloatField(null=False)
    GlucosaPromedio = models.PositiveIntegerField(null=False)

