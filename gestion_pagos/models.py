from django.db import models

# Create your models here.
class Pago(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)
    reserva = models.ForeignKey('gestion_reservas.Reserva', on_delete=models.CASCADE)
    '''
    @property
    def total(self):
        return self.reserva.total if self.reserva else 0.0
    '''
    class Meta:
        db_table = 'pagos'
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        ordering = ['id']