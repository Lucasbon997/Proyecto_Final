from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class PerfilFormulario(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["avatar", "biografia"]  # ✅ solo estos dos


class UsuarioFormulario(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class RecargaTarjetaRegaloFormulario(forms.Form):
    codigo = forms.CharField(
        label="Código de la tarjeta de regalo",
        max_length=50,
    )


class RecargaTarjetaFormulario(forms.Form):
    monto = forms.DecimalField(
        label="Monto a cargar",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text="Use punto para decimales, por ejemplo: 100.50",
    )
    numero_tarjeta = forms.CharField(
        label="Número de tarjeta (ficticio)",
        max_length=19,
        help_text="Puede ser un número inventado, solo dígitos.",
    )
    nombre_titular = forms.CharField(label="Nombre del titular", max_length=100)
    vencimiento = forms.CharField(label="Vencimiento (MM/AA)", max_length=5)
    cvv = forms.CharField(label="CVV", max_length=4)

    def clean_numero_tarjeta(self):
        numero = self.cleaned_data["numero_tarjeta"].replace(" ", "")
        if not numero.isdigit():
            raise forms.ValidationError("El número de tarjeta debe contener solo dígitos.")
        if not (12 <= len(numero) <= 19):
            raise forms.ValidationError(
                "El número de tarjeta debe tener entre 12 y 19 dígitos (puede ser ficticio)."
            )
        return numero

    def clean_vencimiento(self):
        vto = self.cleaned_data["vencimiento"]
        if len(vto) != 5 or vto[2] != "/":
            raise forms.ValidationError("Formato de vencimiento inválido. Use MM/AA.")
        return vto

    def clean_cvv(self):
        cvv = self.cleaned_data["cvv"]
        if not cvv.isdigit() or len(cvv) not in (3, 4):
            raise forms.ValidationError("CVV inválido.")
        return cvv
