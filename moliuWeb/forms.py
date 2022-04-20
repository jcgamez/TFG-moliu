from django import forms
from .models import Game, Posture


class ImportGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["video"]
        widgets = {
            "video": forms.ClearableFileInput(attrs={"style": "display:none"}),
        }


class ClassifyPosture(forms.ModelForm):
    class Meta:
        model = Posture
        fields = "__all__"
        widgets = {
            "score": forms.Select(attrs={"style": "display:none"}),
            "game": forms.Select(attrs={"style": "display:none"}),
            "image": forms.TextInput(attrs={"style": "display:none"}),
        }
