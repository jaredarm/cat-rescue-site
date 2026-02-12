from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django import forms as django_forms
from pathlib import Path
from .models import Application
from .forms import ApplicationForm


# New application for adoption - public
class ApplicationCreateView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'adoptions/application_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        # Support pre-selecting cats via query params: ?cats=1&cats=2
        cats = self.request.GET.getlist('cats')
        if cats:
            initial['cats'] = cats
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Edit an applications form
class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'adoptions/application_form.html'
    success_url = reverse_lazy("application_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Delete an application
class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy("application_list")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ApplicationForm(instance=self.object)
        fieldset_display = []

        def format_field(bound_field):
            field = bound_field.field
            name = bound_field.name
            widget_type = getattr(field.widget, "__class__", type("", (), {})).__name__
            full_width = widget_type in ("Textarea", "ClearableFileInput")
            raw_value = bound_field.value()

            if isinstance(field, django_forms.FileField):
                file_obj = getattr(self.object, name, None)
                if file_obj:
                    return {
                        "label": bound_field.label,
                        "type": "file",
                        "file_url": file_obj.url,
                        "file_name": Path(file_obj.name).name,
                        "full_width": full_width,
                    }
                return {
                    "label": bound_field.label,
                    "type": "text",
                    "value": "None provided",
                    "full_width": full_width,
                }

            if isinstance(field, django_forms.ModelMultipleChoiceField):
                items = []
                if raw_value:
                    items = [str(obj) for obj in field.queryset.filter(pk__in=raw_value)]
                return {
                    "label": bound_field.label,
                    "type": "list",
                    "items": items,
                    "full_width": True,
                }

            if isinstance(field, django_forms.ModelChoiceField):
                if raw_value:
                    try:
                        value = str(field.queryset.get(pk=raw_value))
                    except Exception:
                        value = str(raw_value)
                else:
                    value = "None provided"
                return {
                    "label": bound_field.label,
                    "type": "text",
                    "value": value,
                    "full_width": full_width,
                }

            if isinstance(field, django_forms.BooleanField):
                value = "Yes" if raw_value else "No"
                return {
                    "label": bound_field.label,
                    "type": "text",
                    "value": value,
                    "full_width": full_width,
                }

            if hasattr(field, "choices") and field.choices:
                choices = dict(field.choices)
                value = choices.get(raw_value, raw_value)
            else:
                value = raw_value

            if value in (None, ""):
                value = "None provided"

            return {
                "label": bound_field.label,
                "type": "text",
                "value": value,
                "full_width": full_width,
            }

        for title, opts in form.fieldsets:
            fields = []
            for bound_field in form:
                if bound_field.name in opts.get("fields", ()): 
                    fields.append(format_field(bound_field))

            fieldset_display.append({
                "title": title,
                "description": opts.get("description"),
                "fields": fields,
            })

        context["fieldset_display"] = fieldset_display
        return context
