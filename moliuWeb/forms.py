from django import forms
from .models import Game, Posture
from django.contrib.auth import forms as authForms
from django.core.exceptions import ValidationError
import magic


class LoginForm(authForms.AuthenticationForm):
    username = authForms.UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True, "class": "form-control", "placeholder": "Usuario"}
        )
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        ),
    )


class ImportGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["video"]
        widgets = {
            "video": forms.ClearableFileInput(attrs={"style": "display:none"}),
        }

    def clean_video(self):
        data = self.cleaned_data["video"]
        if magic.from_buffer(data.read(2048), mime=True) != "video/x-msvideo":
            raise (ValidationError('El archivo de la partida debe ser ".avi"'))
        return data


class ClassifyPosture(forms.ModelForm):
    class Meta:
        model = Posture
        fields = "__all__"
        widgets = {
            "score": forms.Select(attrs={"style": "display:none"}),
            "game": forms.Select(attrs={"style": "display:none"}),
            "image": forms.TextInput(attrs={"style": "display:none"}),
            "isScored": forms.CheckboxInput(attrs={"style": "display:none"}),
        }
