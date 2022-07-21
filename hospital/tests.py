import email
from RPA.Desktop.Windows import Windows
from RPA.Desktop import Desktop
from RPA.Browser.Selenium import Selenium
import time
from datetime import datetime
import os
import shutil

import aspose.words as aw


import matplotlib.pyplot as plt2
import re
from os import remove
from django.shortcuts import render




from numpy import empty
from . import models


from tika import parser

win = Windows()
desktop = Desktop()
browser = Selenium()

pathOpera= "C:\Program Files\Google\Chrome\Application\chrome.exe" #se puede cambiar al navegador más comodo
ruta_libreview = "https://www.libreview.com/"
ruta_pdf_word = "https://www.investintech.com/es/productos/a2dpro/"

def PdfText (route, patient, doctor):
    try:
    
        contador= 0
        cont=0
        contador_final= 0
        aux=""
        
        raw = parser.from_file(route)
        
        string = str(raw["content"])
        lista= string.split(" ")
        
        """Ciclo para encontrar GMI""" 

        for text in lista:
            
            if(text== "GMI"):
                break
            contador+=1
       
        aux= lista[contador+1].split("%")
        aux2= str(aux[0])
        nueva = aux2.replace(",",".")
        print(nueva)

        
        Gmi = float(nueva)
    
        print("aqui")
        """Ciclo para encontrar Glucosa promedio"""
        for t in lista:
            if(t.find("Glucosa")!= -1 ) and (lista[cont+1]=="promedio"):
                print(t, " ",lista[cont+1]," ", lista[cont+2])
                break
            cont+=1
        glucosaPromedio= int(lista[cont+2])
    
        print("aqui")
        """Ciclo para encontrar tiempo generado"""
        for te in lista:
            if(te.find("Generado")!= -1):
                print(te, " ",lista[contador_final+1])
                break
            contador_final+=1
        tiempoGenerado= lista[contador_final+1]
        if (tiempoGenerado.find("Informe")!= -1):
            tiempoGenerado = tiempoGenerado.replace("Informe","")
        elif (tiempoGenerado.find("informe")!= -1):
            tiempoGenerado.replace("informe","")

        """Se crea el informe en base a la documentación sacada"""

       

        print("aqui")
        orderReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
        #print(orderReport[0].reportGenerado, " ", models.PatientReport.objects.all())
        if(orderReport.exists()):
            print("aqui")
            if(tiempoGenerado != orderReport[0].reportGenerado):
                print("aqui")
                newPatientReport= models.PatientReport.objects.create(
                patientId= patient.user_id,
                assignedDoctorId= doctor.user.id,
                patientName = patient.user.first_name+" "+patient.user.last_name,
                email= patient.email,
                Type= patient.Type,
                Gmi=Gmi,
                GlucosaPromedio= glucosaPromedio,
                reportGenerado=tiempoGenerado)

                return newPatientReport

            else:
                print("YA EXISTE")
                return empty
        else:
            newPatientReport= models.PatientReport.objects.create(
                patientId= patient.user_id,
                assignedDoctorId= doctor.user.id,
                patientName = patient.user.first_name +" "+patient.user.last_name,
                email= patient.email,
                Type= patient.Type,
                Gmi=Gmi,
                GlucosaPromedio= glucosaPromedio,
                reportGenerado=tiempoGenerado)
            return newPatientReport
    

    except Exception as e:
            print(e)
            print(str(e)) 


def Request(request):
    return render(request, "hospital/loading.html")
    



def isValid(path):
        is_valid = True
        while is_valid:
            try:
                time.sleep(2)
                win.mouse_click_image(path)
                return is_valid
            except Exception as e:
                isValid = False
                print(e)
                print(str(e))

        
def graficoGlucosaPromedio(lista_generado,lista_promedio_glucosa, doctor_id, patient_id, patient):
    fig2, ax2 = plt2.subplots()
    ax2.set_ylabel('Glucosa promedio')
    
    ax2.set_title(patient)
    plt2.bar( lista_generado,lista_promedio_glucosa, color="red")
    now= datetime.now().strftime("%Y-%m-%d")
    route2=f"barraGlucosaPromedio{doctor_id}{patient_id}_{now}.png"

    if(os.path.exists("D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\" + route2)):
        os.remove("D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\" + route2)
        plt2.savefig('D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\'+ route2)
    else:
        plt2.savefig('D:\\the_rial_proyecto\\hospitalmanagement-master\\static\\images\\'+ route2)

def Change_route(namePath, patient, doctor):
    try:
        time.sleep(6)
        if(os.path.exists("D:/the_rial_proyecto/hospitalmanagement-master/hospital/libreview-pdf-word/" + namePath) ):
            return empty
        else:
            shutil.move(
                "C:/Users/carol/Downloads/" + namePath,
                "D:/the_rial_proyecto/hospitalmanagement-master/hospital/libreview-pdf-word/"
                + namePath,
            )
        #PdfText("D:\\the_rial_proyecto\\hospitalmanagement-master\\hospital\\libreview-pdf\\"
        #    + namePath)

        report = PdfText("D:\\the_rial_proyecto\\hospitalmanagement-master\\hospital\\libreview-pdf-word\\"
            + namePath, patient, doctor)

        

        return report

    except Exception as e:
                print(e)
                print(str(e))
        #os.rename(path_str.format(line), path2.format("OK{}".format(line)))

def pdfToWord(patient, doctor):
    try:
        
        time.sleep(6)
        """cambio de nombre para identificarlo"""
        print("pasando")
        Initial_path = str("C:\\Users\\carol\\Downloads")
        now = datetime.now().strftime("%Y-%m-%d")
        filename = max(
                [Initial_path + "\\" + f for f in os.listdir(Initial_path)],
                key=os.path.getctime,
            )
        print(filename)
        namePath = f"report-glucose-libreview_{now}.pdf"
        shutil.move(filename, os.path.join(Initial_path, namePath))
        report = Change_route(namePath, patient, doctor)
        return report
    except Exception as e:
                print(e)
                print(str(e))
    




"""la funcion AppRunInforme se creo con el fin de poder de alguna forma entrar y obtener un informe pero a traves de libreview ya
que las opciones de token, no se pudieron solucionar. esta función solo funciona si el cliente ya tiene cuenta en libreview y ha ingresado otras
veces a libreview, de lo contrario no funcionara ya que antes pedira datos de cookies y del pais"""



def AppRunActualizacion(dict):
     #se puede cambiar al navegador más comodo
    ruta_libreview = "https://www.libreview.com/meter/"
    

    try:
        isValid("hospital\\images\\new_windows.png")
        time.sleep(2)
        desktop.type_text(ruta_libreview)
        desktop.press_keys("enter")
        time.sleep(5)
        desktop.type_text(dict["email"])
        desktop.press_keys("tab")
        desktop.type_text(dict["password"])
        desktop.press_keys("tab")
        time.sleep(4)
        desktop.press_keys("enter")
        time.sleep(5)
        desktop.press_keys("tab")
        time.sleep(2)
        desktop.press_keys("enter")
        time.sleep(2)
        desktop.press_keys("tab")
        desktop.press_keys("tab")
        desktop.press_keys("enter")
        
        return True
    except:
        return False

def AppRunInforme(patient, doctor):

    try:
        isValid("hospital\\images\\new_windows.png")
        time.sleep(2)
        desktop.type_text(ruta_libreview)
        desktop.press_keys("enter")
        time.sleep(5)
        desktop.type_text(patient.libreview_email)
        desktop.press_keys("tab")
        desktop.type_text(patient.libreview_password)
        desktop.press_keys("tab")
        time.sleep(4)
        desktop.press_keys("enter")
        time.sleep(4)
        isValid("hospital\\images\\informes-de-glucosa.png")
        time.sleep(6)
        desktop.press_keys("tab")
        isValid("hospital\\images\\imprimir_pdf.png")
        time.sleep(3)
        isValid("hospital\\images\\click_here.png")
        newPatientReport= pdfToWord(patient, doctor)
        
        
        
        time.sleep(1)
        return newPatientReport
    except:
        return 0
