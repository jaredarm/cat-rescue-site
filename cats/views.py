from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Cat
from .forms import CatForm, CatImage, CatImageForm

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

    def get_success_url(self):
        return reverse_lazy("cat_detail", kwargs={"pk": self.object.pk})


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


def manage_cat_photos(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    images = cat.images.all().order_by("-primary", "-uploaded_at")

    if request.method == "POST":
        form = CatImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.cat = cat
            new_image.save()
            return redirect(reverse("manage_cat_photos", args=[cat.id]))
    else:
        form = CatImageForm()

    return render(request, "cats/manage_photos.html", {
        "cat": cat,
        "images": images,
        "form": form,
    })


def update_cat_image(request, image_id):
    image = get_object_or_404(CatImage, id=image_id)
    cat = image.cat

    if request.method == "POST":
        form = CatImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect(reverse("manage_cat_photos", args=[cat.id]))

    return redirect(reverse("manage_cat_photos", args=[cat.id]))

def delete_cat_image(request, image_id):
    image = get_object_or_404(CatImage, id=image_id)
    cat_id = image.cat.id
    image.delete()
    return redirect(reverse("manage_cat_photos", args=[cat_id]))