from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            dni = form.cleaned_data.get('dni')
            password = form.cleaned_data['password']
            user = authenticate(username=dni, password=password)
            if user:
                login(request, user)
                messages.success(request, "Inicio de sesión exitoso. ¡Bienvenido!")
                return redirect('home')
            else:
                messages.error(request, "Credenciales incorrectas")
        else:
            messages.error(request, "Credenciales incorrectas")
    else:
        form = UserLoginForm()
    return render(request, 'autenticacion/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
