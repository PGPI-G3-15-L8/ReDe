from django.db import models

# Create your models here.
class Pista(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.FloatField()
    category = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.name}'
    class Meta:
        db_table = 'pistas'
        verbose_name = 'pista'
        verbose_name_plural = 'pistas'
        ordering = ['id']
    
