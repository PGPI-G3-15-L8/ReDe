from django.db import migrations
from gestion_reservas.models import Espacio
from django.utils.timezone import make_aware
from django.utils.timezone import now

def create_sample_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')  # Referencia al modelo User
    Reserva = apps.get_model('gestion_reservas', 'Reserva')  # Referencia al modelo Reserva

    # Crear un usuario de prueba
    user = User.objects.create_user(username='testuser', password='12345')
    espacio = Espacio.PADEL
    # Crear reservas de ejemplo

    # Reserva.objects.create(user_id=user, momento_inicio=now, momento_fin=now, espacio=espacio)
    # Reserva.objects.create(user_id=user, momento_inicio=now, momento_fin=now, espacio=espacio)

class Migration(migrations.Migration):
    dependencies = [
        ('gestion_reservas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]

