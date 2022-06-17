import email
from RPA.Desktop.Windows import Windows
from RPA.Desktop import Desktop
from RPA.Browser.Selenium import Selenium
import time
from datetime import datetime
import os
import shutil
import PyPDF2 
import docx
import re
from os import remove

from numpy import empty
from . import models
import requests

win = Windows()
desktop = Desktop()
browser = Selenium()

pathOpera= "C:\\Users\\carol\\AppData\\Local\\Programs\\Opera\\launcher.exe" #se puede cambiar al navegador más comodo
ruta_libreview = "https://www.libreview.com/"
ruta_pdf_word = "https://www.investintech.com/es/productos/a2dpro/"

def PdfText (route, patient, doctor):
    try:
     
        texto = []
        document = docx.Document(route)
        contador= 0
        cont=0
        contador_final= 0
        for parrafo in document.paragraphs:
        # Aquí eliminas los caracteres que no quieres en el párrafo
            p = re.sub(r'[.,:;]', '', parrafo.text)
        # Aquí divides el párrafo en palabras y lo añades a la lista
            texto.extend(p.split())
       
        """Ciclo para encontrar GMI""" 

        for text in texto:
            if(text== "GMI"):
                break
            contador+=1
        aux= texto[contador+1].split("%")
        
        Gmi = int(aux[0])
       
        Gmi = Gmi / 10
    
        """Ciclo para encontrar Glucosa promedio"""
        for t in texto:
            if(t == "Glucosa") and (texto[cont+1]=="promedio"):
                print(t, " ",texto[cont+1]," ", texto[cont+2])
                break
            cont+=1
        glucosaPromedio= int(texto[cont+2])
    

        """Ciclo para encontrar tiempo generado"""
        for te in texto:
            if(te == "Generado"):
                print(te, " ",texto[contador_final+1])
                break
            contador_final+=1
        tiempoGenerado= texto[contador_final+1]

        """Se crea el informe en base a la documentación sacada"""

       

        
        orderReport = models.PatientReport.objects.all().order_by("reportGenerado").reverse()
        #print(orderReport[0].reportGenerado, " ", models.PatientReport.objects.all())
        if(orderReport.exists()):
            if(tiempoGenerado != orderReport[0].reportGenerado):
                newPatientReport= models.PatientReport.objects.create(
                patientId= patient.user_id,
                patientName = patient.user.first_name,
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
                patientName = patient.user.first_name,
                email= patient.email,
                Type= patient.Type,
                Gmi=Gmi,
                GlucosaPromedio= glucosaPromedio,
                reportGenerado=tiempoGenerado)
            return newPatientReport
    

        
        

    except Exception as e:
            print(e)
            print(str(e)) 




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

        

def Change_route(namePath, patient, doctor):
    try:
        time.sleep(4)
        if(os.path.exists("D:/the_rial_proyecto/hospitalmanagement-master/hospital/libreview-pdf-word/" + namePath) ):
            remove("C:/Users/carol/Downloads/" + namePath)
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
    desktop.open_application(pathOpera)
    time.sleep(3)
    desktop.type_text(ruta_pdf_word)
    desktop.press_keys("enter")
    time.sleep(4)
    isValid("hospital\\images\\down.png")
    time.sleep(1)
    isValid("hospital\\images\\down.png")
    time.sleep(1)
    isValid("hospital\\images\\down.png")
    time.sleep(1)
    isValid("hospital\\images\\down.png")
    """cambio de nombre para identificarlo"""
    Initial_path = str("C:\\Users\\carol\\Downloads")
    now = datetime.now().strftime("%Y-%m-%d")
    filename = max(
        [Initial_path + "\\" + f for f in os.listdir(Initial_path)],
        key=os.path.getctime,
    )
    namePath = f"report-glucose-libreview_{now}.pdf"


    print("pasando" + namePath + filename)

    shutil.move(filename, os.path.join(Initial_path, namePath))
    isValid("hospital\\images\\click_word_pdf.png")
    time.sleep(2)
    isValid("hospital\\images\\mostrar-archivos.png")
    time.sleep(2)
    isValid("hospital\\images\\report-name.png")
    desktop.press_keys("enter")
    time.sleep(2)
    time.sleep(22)
    isValid("hospital\\images\\descarga-final.png")
    time.sleep(2)
    namePath2 = f"report-glucose-libreview_{now}.docx"
    if(os.path.exists("C:/Users/carol/Downloads/" + namePath) ):
        remove("C:/Users/carol/Downloads/" + namePath)
    
    report = Change_route(namePath2, patient, doctor)
    return report
    




"""la funcion AppRunInforme se creo con el fin de poder de alguna forma entrar y obtener un informe pero a traves de libreview ya
que las opciones de token, no se pudieron solucionar. esta función solo funciona si el cliente ya tiene cuenta en libreview y ha ingresado otras
veces a libreview, de lo contrario no funcionara ya que antes pedira datos de cookies y del pais"""



def AppRunActualizacion(dict):
    pathOpera= "C:\\Users\\carol\\AppData\\Local\\Programs\\Opera\\launcher.exe" #se puede cambiar al navegador más comodo
    ruta_libreview = "https://www.libreview.com/meter/"
    

    try:
        desktop.open_application(pathOpera)
        time.sleep(3)
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

def AppRunInforme(dict, patient, doctor):

    try:
        desktop.open_application(pathOpera)
        time.sleep(3)
        desktop.type_text(ruta_libreview)
        desktop.press_keys("enter")
        time.sleep(5)
        desktop.type_text(dict["email"])
        desktop.press_keys("tab")
        desktop.type_text(dict["password"])
        desktop.press_keys("tab")
        time.sleep(4)
        desktop.press_keys("enter")
        time.sleep(4)
        isValid("hospital\\images\\informes-de-glucosa.png")
        time.sleep(6)
        desktop.press_keys("tab")
        isValid("hospital\\images\\imprimir_pdf.png")
        time.sleep(3)
        #Change_path()
        newPatientReport= pdfToWord(patient, doctor)
        
        isValid("hospital\\images\\close.png")
        time.sleep(1)
        isValid("hospital\\images\\close_red.png")
        return newPatientReport
    except:
        return 0
