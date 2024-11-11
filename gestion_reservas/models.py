from django.db import models
from django.contrib.auth.models import User

class Espacio(models.TextChoices):
    # tupla para el enumerado
    BALONCESTO = 'Baloncesto', 'Baloncesto'
    FUTBOL = 'Fútbol', 'Fútbol'
    PADEL = 'Padel', 'Padel'
    PISCINA1 = 'Piscina1', 'Piscina1'
    PISCINA2 = 'Piscina2', 'Piscina2'
class Reserva(models.Model):
    espacio=models.CharField(max_length=20, choices=Espacio.choices, default=Espacio.PADEL)
    momento_inicio=models.DateTimeField()
    momento_fin=models.DateTimeField()
    user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Reserva {self.pk} para {self.espacio} de {self.momento_inicio} a {self.momento_fin}'
   
    class Meta:
        db_table = 'reservas'
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ['id'] 
 
class LineaReserva(models.Model):
    reserva = models.ForeignKey('gestion_reservas.Reserva', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.reserva}'     