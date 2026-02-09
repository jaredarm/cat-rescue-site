from .models import Vet
from core.forms import TailwindModelForm


class VetForm(TailwindModelForm):
    class Meta:
        model = Vet
        exclude = (
            "status",
            "submitted_at",
            "reviewed_at",
            "reviewer",
        )
