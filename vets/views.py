from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from .models import Vet
from .forms import VetForm


class VetListView(ListView):
    model = Vet
    template_name = 'vets/vet_list.html'
    context_object_name = 'vets'


class VetCreateView(LoginRequiredMixin, CreateView):
    model = Vet
    form_class = VetForm
    template_name = 'vets/vet_form.html'
    success_url = reverse_lazy("vet_list")


class VetUpdateView(LoginRequiredMixin, UpdateView):
    model = Vet
    form_class = VetForm
    template_name = 'vets/vet_form.html'
    success_url = reverse_lazy("vet_list")


class VetDeleteView(LoginRequiredMixin, DeleteView):
    model = Vet
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("vet_list")
