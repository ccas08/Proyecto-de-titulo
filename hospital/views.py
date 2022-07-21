from queue import Empty
from django.shortcuts import render, redirect, reverse
from numpy import empty
from pymysql import NULL
import os
import shutil
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib.auth import authenticate
from hospital.tests import  AppRunInforme, AppRunActualizacion, graficoGlucosaPromedio
from django.core.exceptions import ValidationError
import matplotlib.pyplot as plt

from datetime import datetime


def validarLetras(value):
    for i in value:
        if not i.isalpha():
            print("aqui")
            raise ValidationError("Este campo solo acepta letras") 

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
        
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
        else:
            userForm = forms.DoctorUserForm(request.POST)
            doctorForm = forms.DoctorForm(request.POST, request.FILES)
            mydict = {"userForm": userForm, "doctorForm": doctorForm}

    return render(request, "hospital/doctorsignup.html", context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    list_diabetes=["Diabetes tipo 1","Diabetes tipo 2", "Diabetes gestacional"]
    mydict = {"userForm": userForm, "patientForm": patientForm , "diabetes": list_diabetes}
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
        else:
            userForm = forms.PatientUserForm(request.POST)
            patientForm = forms.PatientForm(request.POST, request.FILES)
            mydict = {"userForm": userForm, "patientForm": patientForm, "diabetes": list_diabetes}

    return render(request, "hospital/patientsignup.html", context=mydict)



def is_admin(user):
    return user.groups.filter(name="ADMIN").exists()


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


# ---------ser verifica si es paciente admin o doc
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
def inactivar_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status=False
    doctor.save()
    return redirect("admin-view-doctor")


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def delete_report_view(request, pk):
    report = models.PatientReport.objects.get(id=pk)
    report.delete()
    return redirect("patient-view-report")

@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def descargar_ultimo_reporte_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    ) 
    my_dict= {"patient": patient, "boolean":False}
    now= datetime.now().strftime("%Y-%m-%d")
    route=f"report-glucose-libreview_{now}.pdf"
    antigua_ruta= "D:\\the_rial_proyecto\\hospitalmanagement-master\\hospital\libreview-pdf-word\\"+ route
    nueva_ruta= "D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\pdfs\\" + route
    
    if(os.path.exists(antigua_ruta)== False ):
        return render(request, "pacientes\patient_informe_descargar.html", context= my_dict)
    if(os.path.exists("D:/the_rial_proyecto/hospitalmanagement-master/static/pdfs/" + route) ):
        os.remove("D:/the_rial_proyecto/hospitalmanagement-master/static/pdfs/" + route)
        shutil.copy(antigua_ruta, nueva_ruta)
    else:
        shutil.copy(antigua_ruta, nueva_ruta)

    patientReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
    
    for r in patientReport :
        if(patient.user_id == r.patientId):
            boolean= True
            my_dict= {"patient": patient, "boolean":boolean, "route": "/pdfs/"+route}
            
    return render(request, "pacientes\patient_informe_descargar.html", context= my_dict)
    



@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def graficos_view(request):
    patient = models.Patient.objects.get(
        user_id=request.user.id
    ) 
    doctor= models.Doctor.objects.get(
        user_id=patient.assignedDoctorId
    ) 
    
    
    patientReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
    lista_gmi=[]
    nombre= patient.user.first_name + " " + patient.user.last_name
    lista_promedio_glucosa=[]
    lista_generado=[]
    boolean=False
    mydict={"bool":boolean,"patient":patient}
    for r in patientReport :
        if(patient.user_id == r.patientId):
            lista_gmi.append(r.Gmi)
            lista_generado.append(r.reportGenerado)
            lista_promedio_glucosa.append(r.GlucosaPromedio)
            boolean=True
    if(boolean):
        fig, ax = plt.subplots()
        now= datetime.now().strftime("%Y-%m-%d")
        route2=f"barraGlucosaPromedio{doctor.user.id}{patient.user_id}_{now}.png"

        plt.bar( lista_generado,lista_gmi, color="orange")
        ax.set_ylabel('Gmi')
        ax.set_title(nombre)

        route=f"barraGmi{doctor.user.id}{patient.user_id}_{now}.png"
        if(os.path.exists("D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\" + route)):
            print("pasando")
            os.remove("D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\"+ route)
            plt.savefig('D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\'+ route)
        else:
            plt.savefig('D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\'+ route)

        graficoGlucosaPromedio(lista_generado,lista_promedio_glucosa, doctor.user.id,patient.user_id, nombre)

        route_gmi = "/images/" + route
        route_glucosaPromedio = "/images/"+ route2
        mydict={"gmi":route_gmi, "glucosaPromedio":route_glucosaPromedio,"bool":boolean, "patient":patient}

        return render(request, "pacientes/patient_graficos_view.html", context=mydict)
    return render(request, "pacientes/patient_graficos_view.html", context=mydict)



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

@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
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
        
        
        patient.libreview_email = request.POST["libreview_email"]
        patient.libreview_password = request.POST["libreview_password"]
        
        patient.save()
        p = AppRunInforme(patient, doctor)
        if(p!= empty):
            mydict2 = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type, "p": p}  
            mydict.update(mydict2)
            return render(request, "pacientes/dashboard.html", context= mydict)
        else:
            patientReport= models.PatientReport.objects.all().order_by("reportGenerado").reverse()
            mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type, "reports": patientReport }
            return render(request, "hospital/patient_view_report.html", context= mydict)
        
        
    return render(request, "pacientes/patient_datos_libreview_informe.html", context= mydict)

def informe_patient_final_view(request):
    
    patient = models.Patient.objects.get(
        user_id=request.user.id
    ) 
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type}
    
    return mydict

    
    

@login_required(login_url="patientlogin")
@user_passes_test(is_patient)   

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
        return render(request, "pacientes/patient_datos_libreview_actualizacion.html", context= mydict)
        
    return render(request, "pacientes/patient_datos_libreview_actualizacion.html", context=mydict)


def Top3 (id):
    lista2= list()
    lista=list()
    lista3 = list()
    now= datetime.now().strftime("%Y-%m-%d")
    reports= models.PatientReport.objects.all().filter(assignedDoctorId = id).reverse()
    cont=0
    for i in reports:
        if(cont==2):
            break

        suma= "/images/barraGlucosaPromedio"+ str(i.assignedDoctorId) + str(i.patientId) +"_"+ now +".png"
        lista2.append(suma)
        suma= "/images/barraGmi"+ str(i.assignedDoctorId) + str(i.patientId) +"_"+ now +".png"
        lista3.append(suma)
        lista.append(i.patientId)
        cont+=1

    myDict = {"lista_suma_glucosa": lista2,
              "lista_pacientes": lista,
              "lista_suma_gmi": lista3}
    return myDict



# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    reportcount=0
    patientcount = (
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
        .count()
    )
    patient=(
        models.Patient.objects.all()
        .filter(status=True, assignedDoctorId=request.user.id)
    )
    for p in patient:
        report= models.PatientReport.objects.all().filter(patientId = p.user.id)
        for r in report:
            if(p.user.id == r.patientId):
                reportcount+= 1
                
    # for  table in doctor dashboard
    patientdiabetes1count = (
        models.Patient.objects.all()
        .filter(status=True, Type="Diabetes tipo 1")
        .count()
    )
    
    patientdiabetes2count = (
        models.Patient.objects.all()
        .filter(status=True, Type="Diabetes tipo 2")
        .count()
    )
    patientdiabetescount=  patientdiabetes1count + patientdiabetes2count 
    patientgestacionalcount = (
        models.Patient.objects.all()
        .filter(status=True, Type = "Diabetes gestacional")
        .count()
    )
    top3= Top3(request.user.id)
    lista_nombres= list()
    for a in top3["lista_pacientes"]:
        for k in models.Patient.objects.all():
            if k.user.id == a :
                lista_nombres.append(k.user.first_name + " " + k.user.last_name)
    report_doctor= models.PatientReport.objects.all().filter(assignedDoctorId=request.user.id)
    mydict = {
        "patientcount": patientcount,
        "reportcount": reportcount,
        "report_doctor":report_doctor,
        "patientdiabetescount":patientdiabetescount,
        "top3": top3["lista_suma_glucosa"],
        "gmi": top3["lista_suma_gmi"],
        "lista_nombres": lista_nombres,
        "patientgestacionalcount":patientgestacionalcount,
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "doctor/dashboard.html", context=mydict)


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        "doctor": models.Doctor.objects.get(
            user_id=request.user.id
        ),  # for profile picture of doctor in sidebar
    }
    return render(request, "doctor/pacientes.html", context=mydict)

@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def informe_doctor_paciente(request):
    report=models.PatientReport.objects.all().filter(assignedDoctorId = request.user.id)
    patientReport = report.order_by("reportGenerado").reverse()
    doctor = models.Doctor.objects.get(
        user_id=request.user.id
    )  
      # for profile picture of patient in sidebar
    return render(
                request,
                "doctor/reportePacientes.html",
                {"reports": patientReport, "doctor": doctor},
                )
   


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
        "doctor/datosPacientes.html",
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
        mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type}
        now = datetime.now().strftime("%d/%m/%Y")
        for p in patientReport:
            mydict = {"patient": patient, "doctorName": doctor.get_name, "Type": patient.Type, "p": p}      
            return render(request, "pacientes/dashboard.html", context=mydict)

    return render(request, "pacientes/dashboard.html", context=mydict)


def patient_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(
        user_id=request.user.id
    )  # for profile picture of patient in sidebar
    return render(
        request,
        "pacientes/patient_view_doctor.html",
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
                "pacientes/patient_view_report.html",
                {"patient": patient, "reports": patientReport},
                )
    if(valor != True):
        return render(
            request,
            "pacientes/patient_view_report.html",
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
