from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=50,required=True)
    email = forms.EmailField(label='Email',required=True)
    contenido = forms.CharField(label='Contenido', max_length=200, widget=forms.Textarea, required=True)