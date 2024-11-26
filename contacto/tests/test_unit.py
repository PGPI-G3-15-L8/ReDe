from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail
from contacto.forms import ContactForm
from contacto.views import contacto

# Tests para ContactForm
class ContactFormTestCase(TestCase):
    def test_valid_form(self):
        form = ContactForm(data={
            'nombre': 'Test',
            'email': 'test@example.com',
            'contenido': 'Esto es un mensaje de prueba.'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        form = ContactForm(data={
            'nombre': '',
            'email': 'test@example.com',
            'contenido': 'Esto es un mensaje de prueba.'
        })
        self.assertFalse(form.is_valid())

    def test_invalid_form_email_format(self):
        form = ContactForm(data={
            'nombre': 'Test',
            'email': 'email_invalido',
            'contenido': 'Esto es un mensaje de prueba.'
        })
        self.assertFalse(form.is_valid())

# Tests para la vista contacto
class ContactoViewTestCase(TestCase):
    def test_contacto_view_renders_template(self):
        response = self.client.get(reverse('Contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacto/Contacto.html')

    def test_contacto_view_post_valid_data(self):
        response = self.client.post(reverse('Contacto'), data={
            'nombre': 'Test',
            'email': 'test@example.com',
            'contenido': 'Esto es un mensaje de prueba.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('test@example.com', mail.outbox[0].reply_to)

    def test_contacto_view_post_invalid_data(self):
        response = self.client.post(reverse('Contacto'), data={
            'nombre': '',
            'email': 'test@example.com',
            'contenido': 'Esto es un mensaje de prueba.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')


    def test_contacto_view_email_exception_simulated(self):
        response = self.client.post(reverse('Contacto'), data={
            'nombre': 'SimulatedError',
            'email': 'error@example.com',
            'contenido': 'Esto es un mensaje de prueba que forzará un error.'
        })
        self.assertRedirects(response, '/contacto/?no_valido')

# Tests para URLs
class ContactoURLTestCase(TestCase):
    def test_contacto_url_resolves_correct_view(self):
        resolver = resolve(reverse('Contacto'))
        self.assertEqual(resolver.func, contacto)
