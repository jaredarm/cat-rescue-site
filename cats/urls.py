from django.urls import path
from .views import CatCreateView, CatListView, CatDetailView, CatUpdateView, CatDeleteView

urlpatterns = [
    path('', CatListView.as_view(), name='cat_list'),
    path("add/", CatCreateView.as_view(), name="cat_add"),
    path('<int:pk>/', CatDetailView.as_view(), name='cat_detail'),
    path("<int:pk>/edit/", CatUpdateView.as_view(), name="cat_edit"),
    path("<int:pk>/delete/", CatDeleteView.as_view(), name="cat_delete"),
   
]