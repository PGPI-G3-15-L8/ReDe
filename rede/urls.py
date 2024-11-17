"""
URL configuration for rede project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include 
from gestion_reservas.views import reservas_view, crear_reserva_view, modificar_reserva_view, eliminar_reserva_view  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacion.urls')),
    path('reservas/', reservas_view, name='reservas'),
    path('reservas/crear/', crear_reserva_view, name='crear_reserva'),
    path('reservas/modificar/<int:reserva_id>/', modificar_reserva_view, name='modificar_reserva'),
    path('reservas/eliminar/<int:reserva_id>/', eliminar_reserva_view, name='eliminar_reserva'),
    path('contacto/', include('contacto.urls')),
    ]
