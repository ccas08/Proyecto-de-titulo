# Guia para poder iniciar el proyecto

1. Descargar o clonar repositorio
2. Ejecutar los siguientes comandos
<code> 
pip install django==3.0.5 <br/>
pip install django-widget-tweaks <br/>
pip install xhtml2pdf<br>
</code>
3. para encender el proyecto antes se debe hacer estos pasos
<code>
python manage.py makemigrations <br/>
python manage.py migrate <br/>
python manage.py runserver <br/>
</code>

## Cosas a considerar

- El proyecto trabaja con rutas que el usuario a descargar el repositorio no tenga, por lo cual considerar cambiar las rutas puestas

- A la hora de actualizar o bajar los datos del informe, NO MOVER ni el mouse ni teclas, ya que el sistema lo estará haciendo solo

- Las imagenes ocupadas tambien son en base al computador ocupado, por lo cual lo ideal es ocupar el mismo browser que se trabajó ( Opera ), de lo contrario, pueden haber fallas.

- Lo ideal es trabajar con opera o cualquier navegador que no sea chrome por los perfiles que pueden haber, y no dejar cargar la automatización

- Doctores no se termino al completo, por lo cual las vistas no son completas

-La funcionalidad principal es la descarga del informe, que es convertido a docx para obtener los datos, a traves de una pagina (https://www.investintech.com/es/productos/a2dpro/) que nos ayuda a pasar las imagenes del pdf a texto y finalmente poder extraerlo.

- Para que todo funcione, HAY QUE TENER cuenta Libreview para la actualización y ideal para la descarga de datos del informe, datos ya escaneados (puede ser mediante la actualización)

- Se iba a trabajar con Api pero nunca se encontró una manera de poder obtener un token, por lo cual se decidió llegar a tener que usar libreview, pero se sacan los datos mediante automatización.

- Si alguna imagen falla, apagar y enceder denuevo el proyecto( runserver) y si el problema persiste, cambiar la imagen de la ruta





