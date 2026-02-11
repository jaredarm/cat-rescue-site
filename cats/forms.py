from django import forms
from django.http import JsonResponse
from django.db.models import Q
from .models import Cat, CatImage
from common.forms import TailwindModelForm



class CatForm(TailwindModelForm):
    class Meta:
        model = Cat
        fields = "__all__"
        exclude = ["created_by", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CatImageForm(forms.ModelForm):
    class Meta:
        model = CatImage
        fields = ["image", "primary",]
