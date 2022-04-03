from django import forms
from .models import Game


class UploadGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["video"]
        widgets = {
            "video": forms.ClearableFileInput(attrs={"style": "display:none"}),
        }
