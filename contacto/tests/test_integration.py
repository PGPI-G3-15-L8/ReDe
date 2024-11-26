from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from contacto.forms import ContactForm

class ContactoIntegrationTestCase(TestCase):
    def test_contacto_view_get_request(self):
        response = self.client.get(reverse('Contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacto/Contacto.html')
        self.assertIsInstance(response.context['contacto'], ContactForm)

    def test_contacto_view_post_valid_form(self):
        form_data = {
            'nombre': 'Test User',
            'email': 'testuser@example.com',
            'contenido': 'Este es un mensaje de prueba para el formulario de contacto.'
        }
        response = self.client.post(reverse('Contacto'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/contacto/?valido')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Nuevo mensaje de contacto', mail.outbox[0].subject)
        self.assertIn(form_data['contenido'], mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].reply_to, [form_data['email']])

    def test_contacto_view_post_invalid_form(self):
        form_data = {
            'nombre': '',
            'email': 'invalid-email',
            'contenido': 'Este es un mensaje de prueba.'
        }
        response = self.client.post(reverse('Contacto'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacto/Contacto.html')
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertContains(response, 'Introduzca una dirección de correo electrónico válida.')

    def test_contacto_view_post_email_send_failure(self):
        form_data = {
            'nombre': 'Test User',
            'email': 'testuser@example.com',
            'contenido': 'Esto es un mensaje de prueba.'
        }
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend'):
            response = self.client.post(reverse('Contacto'), data=form_data)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, '/contacto/?no_valido')
            self.assertEqual(len(mail.outbox), 0)
