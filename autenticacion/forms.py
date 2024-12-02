from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=9)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")
        password = cleaned_data.get("password")
        user = authenticate(username=dni, password=password)
        if not user:
            raise forms.ValidationError("Credenciales incorrectas")
        return cleaned_data