from django.urls import path
from .views import VetListView

urlpatterns = [
    path('', VetListView.as_view(), name='vet_list'),
]