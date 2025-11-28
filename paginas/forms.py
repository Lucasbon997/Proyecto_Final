from django import forms
from .models import Reseña

class ReseñaFormulario(forms.ModelForm):
    # Campo visible para el usuario (like / dislike)
    OPINIONES = (
        ("like", "Me gustó 👍"),
        ("dislike", "No me gustó 👎"),
    )
    opinion = forms.ChoiceField(
        choices=OPINIONES,
        widget=forms.RadioSelect,
        label="¿Qué te pareció el producto?",
    )

    class Meta:
        model = Reseña
        fields = ["texto"]  # solo texto del modelo
        labels = {
            "texto": "Tu reseña",
        }
        widgets = {
            "texto": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Escribe aquí tu opinión sobre el producto...",
            }),
        }
