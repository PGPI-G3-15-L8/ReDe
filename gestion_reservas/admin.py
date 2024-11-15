from django.contrib import admin
from .models import Reserva, LineaReserva
# Register your models here.
class ReservaAdmin(admin.ModelAdmin):
    readonly_fields=('created_at',)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(LineaReserva)
