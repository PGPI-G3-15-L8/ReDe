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


class UserRegistrationForm(forms.ModelForm):
    dni = forms.CharField(label="DNI", max_length=9)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['dni', 'password']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if User.objects.filter(username=dni).exists():
            raise forms.ValidationError("Este DNI ya está registrado.")
        return dni

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


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
