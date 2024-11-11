from django.contrib import admin
from gestion_reservas.models import Reserva, LineaReserva
from gestion_pagos.models import Pago
from gestion_pistas.models import Pista
# Register your models here.
admin.register(Reserva)
admin.register(LineaReserva)
admin.register(Pago)
admin.register(Pista)
