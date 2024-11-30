from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Ruta vacía para la página principal
    path('privacy-policy/', views.privacy_policy_view, name='privacy-policy'),  # Ruta para la política de privacidad
    path('about-us/', views.about_us_view, name='about-us'),  # Ruta para la página de acerca de nosotros
]