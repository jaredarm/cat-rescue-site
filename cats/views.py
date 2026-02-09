from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Cat
from .forms import CatForm, CatImageFormSet

queryset = Cat.objects.prefetch_related('images')

class CatListView(ListView):
    model = Cat
    template_name = 'cats/cat_list.html'
    context_object_name = 'cats'

    def get_queryset(self):
        qs = Cat.objects.all()
        parameters = self.request.GET

        if parameters.get("vaccinated"):
            qs = qs.filter(is_vaccinated=True)

        if parameters.get("microchipped"):
            qs = qs.filter(is_microchipped=True)

        if parameters.get("sterilised"):
            qs = qs.filter(is_sterilised=True)

        if parameters.get("fiv_positive"):
            qs = qs.filter(is_fiv_positive=True)

        if parameters.get("good_with_kids"):
            qs = qs.filter(is_good_with_kids=True)

        if parameters.get("good_with_dogs"):
            qs = qs.filter(is_good_with_dogs=True)

        if parameters.get("good_with_cats"):
            qs = qs.filter(is_good_with_cats=True)

        return qs

class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/cat_detail.html'

class CatUpdateView(LoginRequiredMixin, UpdateView):
    model = Cat
    form_class = CatForm
    template_name = "cats/cat_form.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context["image_formset"] = CatImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
    #     else:
    #         context["image_formset"] = CatImageFormSet(instance=self.object)
    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     image_formset = context["image_formset"]

    #     if image_formset.is_valid():
    #         self.object = form.save()
    #         image_formset.instance = self.object
    #         image_formset.save()
    #         return redirect("cat_detail", pk=self.object.pk)

    #     return self.form_invalid(form)    

class CatCreateView(LoginRequiredMixin, CreateView):
    model = Cat
    form_class = CatForm
    template_name = "cats/cat_form.html"

    def get_success_url(self):
        return reverse_lazy("cat_detail", kwargs={"pk": self.object.pk})
    
class CatDeleteView(LoginRequiredMixin, DeleteView):
    model = Cat
    template_name = "cat_confirm_delete.html"
    success_url = reverse_lazy("cat_list")