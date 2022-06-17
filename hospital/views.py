from queue import Empty
from tkinter import Button
from django.shortcuts import render, redirect, reverse
from numpy import empty
from pymysql import NULL
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from hospital.tests import  AppRunInforme, AppRunActualizacion

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    #AppRun()
    return render(request, "hospital/index.html")


# for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/adminclick.html")


# for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/doctorclick.html")


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "hospital/patientclick.html")


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == "POST":
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name="ADMIN")
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect("adminlogin")
    return render(request, "hospital/adminsignup.html", {"form": form})


def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect("doctorlogin")
    return render(request, "hospital/doctorsignup.html", context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect("patientlogin")
    return render(request, "hospital/patientsignup.html", context=mydict)


# -----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("doctor-dashboard")
        else:
            return render(request, "hospital/doctor_wait_for_approval.html")
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(
            user_id=request.user.id, status=True
        )
        if accountapproval:
            return redirect("patient-dashboard")
        else:
            return render(request, "hospital/patient_wait_for_approval.html")


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by("-id")
    patients = models.Patient.objects.all().order_by("-id")
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    mydict = {
        "doctors": doctors,
        "patients": patients,
        "doctorcount": doctorcount,
        "pendingdoctorcount": pendingdoctorcount,
        "patientcount": patientcount,
        "pendingpatientcount": pendingpatientcount,
    }
    return render(request, "hospital/admin_dashboard.html", context=mydict)


# this view for sidebar click on admin page
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, "hospital/admin_doctor.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-view-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect("admin-view-doctor")
    return render(request, "hospital/admin_update_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {"userForm": userForm, "doctorForm": doctorForm}
    if request.method == "POST":
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name="DOCTOR")
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-doctor")
    return render(request, "hospital/admin_add_doctor.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, "hospital/admin_approve_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse("admin-approve-doctor"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect("admin-approve-doctor")



@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, "hospital/admin_patient.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, "hospital/admin_view_patient.html", {"patients": patients})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()
            return redirect("admin-view-patient")
    return render(request, "hospital/admin_update_patient.html", context=mydict)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {"userForm": userForm, "patientForm": patientForm}
    if request.method == "POST":
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get("assignedDoctorId")
            patient.save()

            my_patient_group = Group.objects.get_or_create(name="PATIENT")
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect("admin-view-patient")
    return render(request, "hospital/admin_add_patient.html", context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(
        request, "hospital/admin_approve_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse("admin-approve-patient"))


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect("admin-approve-patient")


def informe_patient_view(request):
   
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type}
    if request.method == "POST":
        postDict = {
            "email": request.POST["libreview_email"],
            "password": request.POST["libreview_password"]
        }
        mydict.update(postDict)
        
        pT = models.Patient()
        pT.libreview_email = request.POST["libreview_email"]
        pT.libreview_password = request.POST["libreview_password"]
        p=AppRunInforme(mydict, patient, doctor)
        if(p != empty):
            report = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type,"Gmi": p.Gmi, "glucosaPromedio": p.GlucosaPromedio , "fechaGenerada" : p.reportGenerado, "email": patient.email}
            mydict.update(report)

            return render(request, "hospital/patient_dashboard.html", context= mydict)
        else:
            report = {"patient": patient, "reports": models.PatientReport(), "patient_id": patient.user_id}
            mydict.update(report)
            return render(request, "hospital/patient_view_report.html", context= mydict)
        
    return render(request, "hospital/patient_datos_libreview_informe.html", context=mydict)


def actualizacion_patient_view(request):
    """patients = models.Patient.objects.all().filter(status=True)
    
    return render(
        request, "hospital/patient_datos_libreview.html", {"patients": patients}
    )"""
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type}
    if request.method == "POST":
        postDict = {
            "email": request.POST["libreview_email"],
            "password": request.POST["libreview_password"]
        }
        mydict.update(postDict)
       
        pT = models.Patient()
        pT.libreview_email = request.POST["libreview_email"]
        pT.libreview_password = request.POST["libreview_password"]
        AppRunActualizacion(mydict)
        return render(request, "hospital/patient_datos_libreview_actualizacion.html", context= mydict)
        
    return render(request, "hospital/patient_datos_libreview_actualizacion.html", context=mydict)




# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .count()
    )
    # for  table in doctor dashboard
    
    mydict = {
        "patientcount": patientcount,
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_dashboard.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "hospital/doctor_patient.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(
        status=True, assignedDoctorId=request.user.id
    )
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def search_view(request):
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  # for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET["query"]
    patients = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .filter(Q(Type__icontains=query) | Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients, "doctor": doctor},
    )



# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    patientReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
    if(patientReport == Empty) or (patientReport == NULL) or (patientReport== None) or (not(patientReport.exists())):
       mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type}
       print("aqui")
    else:
        mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type, "reports": patientReport}      
        return render(request, "hospital/patient_dashboard.html", context=mydict)

    return render(request, "hospital/patient_dashboard.html", context=mydict)


def patient_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )
def patient_view_reports_view(request):
    patientReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    valor = False
    for p in patientReport:
        if(p.patientId == request.user.id ):
            valor = True
            return render(
                request,
                "hospital/patient_view_report.html",
                {"patient": patient, "reports": patientReport},
                )
    if(valor != True):
        return render(
            request,
            "hospital/patient_view_report.html",
            {"patient": patient},
            )           


def search_doctor_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar

    # whatever user write in search box we get in query
    query = request.GET["query"]
    doctors = (
        models.Doctor.objects.all()
        .filter(status=True)
        .filter(Q(user__first_name__icontains=query))
    )
    return render(
        request,
        "hospital/patient_view_doctor.html",
        {"patient": patient, "doctors": doctors},
    )





# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------
