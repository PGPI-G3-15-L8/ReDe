from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    dni = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}[A-Z]$',
                message='El DNI debe tener 8 dígitos seguidos de una letra (ejemplo: 12345678A)'
            )
        ]
    )

    def __str__(self):
        return self.username
