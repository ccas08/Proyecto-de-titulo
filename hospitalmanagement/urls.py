from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView


# -------------FOR ADMIN RELATED URLS
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name=""),
    path("adminclick", views.adminclick_view),
    path("doctorclick", views.doctorclick_view),
    path("patientclick", views.patientclick_view),
    path("adminsignup", views.admin_signup_view),
    path("doctorsignup", views.doctor_signup_view, name="doctorsignup"),
    path("patientsignup", views.patient_signup_view),
    path("adminlogin", LoginView.as_view(template_name="hospital/adminlogin.html")),
    path("doctorlogin", LoginView.as_view(template_name="hospital/doctorlogin.html")),
    path("patientlogin", LoginView.as_view(template_name="hospital/patientlogin.html")),
    path("afterlogin", views.afterlogin_view, name="afterlogin"),
    path(
        "logout", LogoutView.as_view(template_name="hospital/index.html"), name="logout"
    ),
    path("admin-dashboard", views.admin_dashboard_view, name="admin-dashboard"),
    path("admin-doctor", views.admin_doctor_view, name="admin-doctor"),
    path("admin-view-doctor", views.admin_view_doctor_view, name="admin-view-doctor"),
    path(
        "delete-doctor-from-hospital/<int:pk>",
        views.delete_doctor_from_hospital_view,
        name="delete-doctor-from-hospital",
    ),
    path(
        "delete-report/<int:pk>",
        views.delete_report_view,
        name="delete-report",
    ),
    path("update-doctor/<int:pk>", views.update_doctor_view, name="update-doctor"),
    path("admin-add-doctor", views.admin_add_doctor_view, name="admin-add-doctor"),
    path(
        "admin-approve-doctor",
        views.admin_approve_doctor_view,
        name="admin-approve-doctor",
    ),
    path("approve-doctor/<int:pk>", views.approve_doctor_view, name="approve-doctor"),
    path("reject-doctor/<int:pk>", views.reject_doctor_view, name="reject-doctor"),
    path("admin-patient", views.admin_patient_view, name="admin-patient"),
    path(
        "admin-view-patient", views.admin_view_patient_view, name="admin-view-patient"
    ),
    path(
        "delete-patient-from-hospital/<int:pk>",
        views.delete_patient_from_hospital_view,
        name="delete-patient-from-hospital",
    ),
    path("update-patient/<int:pk>", views.update_patient_view, name="update-patient"),
    path("admin-add-patient", views.admin_add_patient_view, name="admin-add-patient"),
    path(
        "admin-approve-patient",
        views.admin_approve_patient_view,
        name="admin-approve-patient",
    ),
    path(
        "approve-patient/<int:pk>", views.approve_patient_view, name="approve-patient"
    ),
    path("reject-patient/<int:pk>", views.reject_patient_view, name="reject-patient"),
    path(
        "informe-patient",
        views.informe_patient_view,
        name="informe-patient",
    ),
    path(
        "patient-graficos",
        views.graficos_view,
        name="patient-graficos",
    ),
    path(
        "patient-descargar-informe",
        views.descargar_ultimo_reporte_view,
        name="patient-descargar-informe",
    ),
    path(
        "loading-page-informe",
        views.informe_patient_final_view,
        name="informe-final-patient",
    ),
    path(
        "actualizacion-patient",
        views.actualizacion_patient_view,
        name="actualizacion-patient",
    ),

]


# ---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path("doctor-dashboard", views.doctor_dashboard_view, name="doctor-dashboard"),
    path("search", views.search_view, name="search"),
    path("doctor-patient", views.doctor_patient_view, name="doctor-patient"),
    path(
        "doctor-view-patient",
        views.doctor_view_patient_view,
        name="doctor-view-patient",
    ),

    
]


# ---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [
    path("patient-dashboard", views.patient_dashboard_view, name="patient-dashboard"),
    path(
        "patient-view-doctor",
        views.patient_view_doctor_view,
        name="patient-view-doctor",
    ),
    path(
        "patient-view-report",
        views.patient_view_reports_view,
        name="patient-view-report",
    ),
    path("searchdoctor", views.search_doctor_view, name="searchdoctor"),
    
]
