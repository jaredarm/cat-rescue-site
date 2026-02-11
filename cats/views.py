from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = self.object

        # Provide bonded cat IDs as a simple Python list
        context["bonded_cat_ids"] = list(cat.bonded_cats.values_list("id", flat=True))

        return context

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
    images = cat.images.all()

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


def reorder_cat_images(request, cat_id):
    if request.method == "POST":
        order = request.POST.getlist("order[]")  # array of IDs

        for index, image_id in enumerate(order):
            CatImage.objects.filter(
                id=image_id, cat_id=cat_id).update(order=index)

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def set_primary_image(request, image_id):
    image = get_object_or_404(CatImage, id=image_id)
    cat = image.cat

    if request.method == "POST":
        # Mark this image as primary
        image.primary = True
        image.save()  # Your model's save() already unsets others

    return redirect("manage_cat_photos", cat_id=cat.id)

def search_cats(request):
    q = request.GET.get("q", "")
    results = []

    if q:
        cats = Cat.objects.filter(name__icontains=q).prefetch_related('bonded_cats')[:10]
        results = [
            {
                "id": c.id,
                "name": c.name,
                "status": c.status,
                "bonded_cats": list(c.bonded_cats.values_list("id", flat=True)),
                "primary_image": (c.primary_image.image.url if c.primary_image else None),
                "fostered_in": c.fostered_in,
                "age": c.age,
            }
            for c in cats
        ]

    return JsonResponse(results, safe=False)

def get_cats_by_ids(request):
    ids = request.GET.getlist("ids[]", [])
    cats = Cat.objects.filter(id__in=ids).prefetch_related('bonded_cats')
    data = [
        {
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "bonded_cats": list(c.bonded_cats.values_list("id", flat=True)),
            "primary_image": (c.primary_image.image.url if c.primary_image else None),
            "fostered_in": c.fostered_in,
            "age": c.age,
        }
        for c in cats
    ]
    return JsonResponse(data, safe=False)