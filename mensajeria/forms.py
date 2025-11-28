from django import forms
from .models import Mensaje
from django.contrib.auth.models import User

class MensajeFormulario(forms.ModelForm):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Mensaje
        fields = ["destinatario", "asunto", "cuerpo"]
