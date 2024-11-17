from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm

def contacto(request):
    if request.method == 'POST':
        contacto = ContactForm(data=request.POST)
        if contacto.is_valid():
            name = request.POST.get('nombre')
            email = request.POST.get('email')
            content = request.POST.get('contenido')
            email_message = EmailMessage(
                'ReDe: Nuevo mensaje de contacto',
                'El usuario con nombre {} con la dirección de correo {} escribe lo siguiente:\n\n{}'.format(name, email, content),
                '', ['atencion.contacto.rede@gmail.com'], reply_to=[email]
            )
            try:
                email_message.send()
                return redirect('/contacto/?valido')
            except:
                return redirect('/contacto/?no_valido')
    else:
        contacto = ContactForm()

    return render(request, 'contacto/Contacto.html', {'contacto': contacto})