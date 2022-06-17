from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to="profile_pic/DoctorProfilePic/", null=True, blank=True
    )
    email = models.CharField(max_length=60)
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
        upload_to="profile_pic/PatientProfilePic/", null=True, blank=True
    )
    email = models.CharField(max_length=60)
    Type = models.CharField(max_length=100, null=False)
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
    patientName = models.CharField(max_length=40)
    email = models.CharField(max_length=60)
    Type = models.CharField(max_length=100, null=True)
    reportGenerado= models.CharField(max_length=20, null=True)
    Gmi = models.FloatField(null=False)
    GlucosaPromedio = models.PositiveIntegerField(null=False)

