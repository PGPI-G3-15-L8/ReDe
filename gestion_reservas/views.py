# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva, Espacio
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.utils.timezone import now
import json

# TODO: descomentar los login_required
# @login_required
def reservas_view(request):
    user = User.objects.filter(username='testuser').first()
    # reservas = Reserva.objects.filter(user_id=request.user)
    reservas = Reserva.objects.filter(user_id = user)
    return render(request, 'gestion_reservas.html', {'reservas': reservas})

# @login_required
def crear_reserva_view(request):
    # en el formulario hay que usar el formato '2024-01-01T14:00:00''
    data = json.loads(request.body)
    momento_inicio = data.get('momento_inicio')
    momento_fin = data.get('momento_fin')
    espacio_str = data.get('espacio')

    espacio = evaluate(espacio_str)
    momento_inicio_naive = datetime.fromisoformat(momento_inicio)
    momento_fin_naive = datetime.fromisoformat(momento_fin)

    momento_inicio_aware = make_aware(momento_inicio_naive)
    momento_fin_aware = make_aware(momento_fin_naive)

    created_at = now()

    user = User.objects.filter(username='testuser').first()

    resultado_validacion = validate_post(user, momento_inicio_aware, momento_fin_aware, espacio)
    if resultado_validacion is not None:
        return resultado_validacion

    reserva = Reserva.objects.create(
        # user_id=request.user,
        user_id=user,
        momento_inicio=momento_inicio_aware,
        momento_fin=momento_fin_aware,
        espacio=espacio,
        created_at=created_at
    )

    return JsonResponse({
        "id": reserva.id,
        "momento_inicio": reserva.momento_inicio,
        "momento_fin": reserva.momento_fin,
        "espacio": reserva.espacio,
        "created_at": reserva.created_at
    }, status=201)

# @login_required
def modificar_reserva_view(request, reserva_id):
    # reserva = Reserva.objects.get(id=reserva_id, user_id=request.user)
    user = User.objects.filter(username='testuser').first()
    reserva = Reserva.objects.get(id=reserva_id, user_id = user)
    data = json.loads(request.body)
    momento_inicio = data.get('momento_inicio')
    if momento_inicio:
        momento_inicio_naive = datetime.fromisoformat(momento_inicio)
        momento_inicio_aware = make_aware(momento_inicio_naive)
        reserva.momento_inicio = momento_inicio_aware
    momento_fin = data.get('momento_fin')
    if momento_fin:
        momento_fin_naive = datetime.fromisoformat(momento_fin)
        momento_fin_aware = make_aware(momento_fin_naive)
        reserva.momento_fin = momento_fin_aware
    espacio_str = data.get('espacio')
    if espacio_str:
        reserva.espacio = evaluate(espacio_str)

    resultado_validacion = validate_put(user, reserva, data)
    if resultado_validacion is not None:
        return resultado_validacion
    reserva.save()

    return JsonResponse({
        "id": reserva.id,
        "momento_inicio": reserva.momento_inicio,
        "momento_fin": reserva.momento_fin,
        "espacio": reserva.espacio
    })

# @login_required
def eliminar_reserva_view(request, reserva_id):
    # reserva = Reserva.objects.get(id=reserva_id, user_id=request.user)
    user = User.objects.filter(username='testuser').first()
    reserva = Reserva.objects.get(id=reserva_id, user_id = user)
    reserva.delete()
    return JsonResponse({"success": True}, status=200)

def evaluate(pista_str):
    match pista_str:
        case 'Baloncesto':
            return Espacio.BALONCESTO
        case 'Fútbol':
            return Espacio.FUTBOL
        case 'Padel':
            return Espacio.PADEL
        case 'Piscina1':
            return Espacio.PISCINA1
        case 'Piscina2':
            return Espacio.PISCINA2

def validate_post(user, momento_inicio, momento_fin, espacio):
    if momento_fin - momento_inicio != timedelta(hours=1):
        return JsonResponse({"error": "La reserva debe durar una hora"})
    if Reserva.objects.filter(user_id=user).count() >= 10:
        return JsonResponse({"error": "No puedes tener más de 3 reservas"})
    if Reserva.objects.filter(espacio=espacio, momento_inicio=momento_inicio, momento_fin=momento_fin).exists():
        return JsonResponse({"error": "Ya existe una reserva en ese momento"})
    # la reserva tiene que ser en el futuro:
    if momento_inicio < now() or momento_fin < now():
        return JsonResponse({"error": "La reserva tiene que ser en el futuro"})
    if Reserva.objects.filter(espacio=espacio, momento_inicio=momento_inicio, momento_fin=momento_inicio).exists():
        return JsonResponse({"error": "Ya existe una reserva en ese momento"})
    # momento_inicio y momento_fin tiene que ser una hora entera y 0 minutos:
    if momento_inicio.minute != 0 or momento_fin.minute != 0:
        return JsonResponse({"error": "La reserva tiene que empezar y terminar en punto"})
    return None

def validate_put(user, reserva, data):
    if data.get('momento_inicio'):
        momento_inicio = make_aware(datetime.fromisoformat(data.get('momento_inicio')))
        if reserva.momento_fin - momento_inicio != timedelta(hours=1):
            return JsonResponse({"error": "La reserva debe durar una hora"})
        if momento_inicio < now():
            return JsonResponse({"error": "La reserva tiene que ser en el futuro"})
        if momento_inicio.minute != 0:
            return JsonResponse({"error": "La reserva tiene que empezar en punto"})

    if data.get('momento_fin'):
        momento_fin = make_aware(datetime.fromisoformat(data.get('momento_fin')))
        if momento_fin - reserva.momento_inicio != timedelta(hours=1):
            return JsonResponse({"error": "La reserva debe durar una hora"})
        if momento_fin < now():
            return JsonResponse({"error": "La reserva tiene que ser en el futuro"})
        if momento_fin.minute != 0:
            return JsonResponse({"error": "La reserva tiene que terminar en punto"})

    if Reserva.objects.filter(user_id=user).count() >= 3:
        return JsonResponse({"error": "No puedes tener más de 3 reservas"})
   
    espacio = evaluate(data.get('espacio')) if data.get('espacio') else reserva.espacio
    momento_inicio = make_aware(datetime.fromisoformat(data.get('momento_inicio')) if data.get('momento_inicio') else reserva.momento_inicio)
    momento_fin = make_aware(datetime.fromisoformat(data.get('momento_fin')) if data.get('momento_fin') else reserva.momento_fin)
    if Reserva.objects.filter(espacio=espacio, momento_inicio=momento_inicio, momento_fin=momento_fin).exists():
        return JsonResponse({"error": "Ya existe una reserva en ese momento"})
    return None
