from django.views.generic import ListView
from .models import Vet


class VetListView(ListView):
    model = Vet
    template_name = 'vets/vet_list.html'
    context_object_name = 'vets'
