<p align="center">
   <img src="images/escudo.png" alt="Escudo" width="125"/>
   <img src="images/logo.png" alt="Logo" width="200"/>
</p>

# ReDe - Reservas Deportivas para Villanueva de las Cruces

Bienvenido a **ReDe**, tu aplicación para gestionar reservas deportivas de manera eficiente y accesible desde cualquier dispositivo. Este documento te guiará a través de las funcionalidades y características principales de la aplicación.

---

# Índice

1. [Clonación del repositorio de código fuente](#1-clonación-del-repositorio-de-código-fuente)
2. [Preparación de los archivos de configuración](#2-preparación-de-los-archivos-de-configuración)
3. [Despliegue en Render](#3-despliegue-en-render)


---

## 1. Clonación del repositorio de código fuente

Ejecute el siguiente comando desde una terminal:
- **git clone https://github.com/PGPI-G3-15-L8/ReDe.git**

## 2. Preparación de los archivos de configuración

Una vez desarrollada la aplicación web, se han de seguir los siguientes pasos.
- **Instalar las dependencias whitenoise y gunicorn:** Ejecute los comandos **pip install whitenoise** y **pip install gunicorn** desde una terminal
- **Generar el archivo con las dependencias del proyecto:** Abra una terminal desde la carpeta que contiene el proyecto (en este caso, rede) e introduzca el siguiente comando:
**pip freeze > requirements.txt**.  
Posteriormente se puede continuar añadiendo dependencias en caso de ser necesario.
Por cada cambio en este archivo, se han de subir los cambios al repositorio para permitir su posterior instalación desde la plataforma de despliegue.

- **Recopilar los archivos estáticos:** Para ello, siga estos dos pasos:
   1) Vaya al archivo **settings.py** del proyecto e incluya lo siguiente:

      A continuación de **STATIC_URL:**
      - **STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]**
      - **STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')**
      
      En la lista de **middlewares:**
      - **'whitenoise.middleware.WhiteNoiseMiddleware',**
   
   2) Desde la terminal, introduzca el comando **python manage.py collectstatic**, verá que se genera una carpeta llamada **staticfiles** una vez ejecutado el comando.

Una vez realizado esto, haga **git push** para incluir estos nuevos cambios en el repositorio, asegúrese de incluirlos en la **rama main**

## 3. Despliegue en Render

Acceda al sitio web de Render con el siguiente enlace: https://render.com/ y cree su cuenta vinculándola con su usuario de Github o inicie sesión si ya tenía una cuenta en Render.

Una vez hecho esto, siga los siguientes pasos:

1) **Crear un servicio web**: Para ello, haga click en **new** y posteriormente **web service**
2) **Seleccione el repositorio de github del proyecto**: En este caso **PGPI-G3-15-L8/ReDe** y haga click en connect
3) **Indique un nombre para el servicio web**
4) **Seleccione Python 3 como lenguaje**
5) **Seleccione la rama main para el despliegue**
6) **Indique el comando de inicio: gunicorn rede.wsgi**
7) **Escoja el tipo de instancia**
8) **Haga click en Deploy Web Service**

Una vez realizado esto comenzará a construirse el proyecto y será desplegado en la url que se le indica.

---

ReDe es tu solución completa para la gestión de reservas deportivas. ¡Gracias por confiar en nosotros!