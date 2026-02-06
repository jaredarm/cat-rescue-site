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
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the current filter + all statuses to the template
        context["current_status"] = self.request.GET.get("status", "")
        context["status_choices"] = Application._meta.get_field(
            "status").choices

        return context


# Detail view of application - logged in only
class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'adoptions/application_detail.html'
