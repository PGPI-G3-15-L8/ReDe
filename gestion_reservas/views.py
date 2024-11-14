# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva
from django.http import JsonResponse
from datetime import date

@login_required
def reservas_view(request):
    reservas = Reserva.objects.filter(user=request.user)
    return render(request, 'reservas/reservas.html', {'reservas': reservas})

@login_required
def crear_reserva_view(request):
    fecha_inicio = request.POST.get('fecha_inicio')
    fecha_fin = request.POST.get('fecha_fin')
    pista = request.POST.get('pista')

    reserva = Reserva.objects.create(
        user=request.user,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        pista=pista
    )

    return JsonResponse({
        "id": reserva.id,
        "fecha_inicio": reserva.fecha_inicio,
        "fecha_fin": reserva.fecha_fin,
        "pista": reserva.pista
    }, status=201)

@login_required
def modificar_reserva_view(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id, user=request.user)
    reserva.fecha_inicio = request.POST.get('fecha_inicio', reserva.fecha_inicio)
    reserva.fecha_fin = request.POST.get('fecha_fin', reserva.fecha_fin)
    reserva.pista = request.POST.get('pista', reserva.pista)
    reserva.save()

    return JsonResponse({
        "id": reserva.id,
        "fecha_inicio": reserva.fecha_inicio,
        "fecha_fin": reserva.fecha_fin,
        "pista": reserva.pista
    })

@login_required
def eliminar_reserva_view(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id, user=request.user)
    reserva.delete()
    return JsonResponse({"success": True}, status=204)

