from django import forms
from django.forms import inlineformset_factory
from .models import Cat, CatImage

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = "__all__"
        exclude = ["created_by", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

CatImageFormSet = inlineformset_factory(
    Cat,
    CatImage,
    fields=["image", "caption", "primary"],
    extra=1,
    can_delete=True
)
