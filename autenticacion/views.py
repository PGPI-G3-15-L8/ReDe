from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "¡Registro completado con éxito!")
            return redirect('home')
        else:
            messages.error(request, "Error en el formulario. Verifique los datos.")
    else:
        form = UserRegistrationForm()
    return render(request, 'autenticacion/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get('username')
            clave = form.cleaned_data.get('password')
            usuario = authenticate(username=nombre, password=clave)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f"Bienvenido {nombre}")
                return redirect('home')
            else:
                messages.error(request, "Credenciales incorrectas")
        else:
            messages.error(request, "Error en el formulario")
    else:
        form = AuthenticationForm()
    return render(request, 'autenticacion/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
