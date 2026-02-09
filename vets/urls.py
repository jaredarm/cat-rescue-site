from django.urls import path
from .views import VetListView, VetDeleteView, VetUpdateView, VetCreateView

urlpatterns = [
    path('', VetListView.as_view(), name='vet_list'),
    path("add/", VetCreateView.as_view(), name="vet_add"),
    path("<int:pk>/edit/", VetUpdateView.as_view(), name="vet_edit"),
    path("<int:pk>/delete/", VetDeleteView.as_view(), name="vet_delete"),
]