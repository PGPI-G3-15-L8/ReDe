from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    dni = forms.CharField(max_length=9, label="DNI")

    class Meta:
        model = Usuario
        #fields = ['username', 'email', 'dni', 'password1', 'password2']
        fields = ['dni', 'password1', 'password2']


    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Este DNI ya está registrado.")
        return dni
