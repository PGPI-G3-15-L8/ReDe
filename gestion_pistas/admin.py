from django.contrib import admin
from .models import Pista
# Register your models here.
class PistaAdmin(admin.ModelAdmin):
    readonly_fields=('created_at')
    search_fields = ['name']
admin.register(Pista, PistaAdmin)