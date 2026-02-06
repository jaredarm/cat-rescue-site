from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Application
from .forms import ApplicationForm


# New application for adoption - public
class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "adoptions/application_add.html"


# List view - logged in only
class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'adoptions/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.all()


# Detail view of application - logged in only
class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'adoptions/application_detail.html'
