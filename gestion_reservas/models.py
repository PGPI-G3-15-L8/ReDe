from django.db import models

class Reserva(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    #client = models.ForeignKey('autenticacion.User', on_delete=models.CASCADE)
    pista = models.ForeignKey('gestion_pistas.Pista', on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return f'{self.client} - {self.pista} - {self.date}'
    @property
    def total(self):
        return self.pista.price if self.pista else 0.0
    class Meta:
        db_table = 'reservas'
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        ordering = ['id'] 
 
class LineaReserva(models.Model):
    reserva = models.ForeignKey('gestion_reservas.Reserva', on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.reserva}'     