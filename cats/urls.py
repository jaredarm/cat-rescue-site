from django.urls import path
from .views import CatCreateView, CatListView, CatDetailView, CatUpdateView, CatDeleteView
from . import views

urlpatterns = [
    path('', CatListView.as_view(), name='cat_list'),
    path("add/", CatCreateView.as_view(), name="cat_add"),
    path('<int:pk>/', CatDetailView.as_view(), name='cat_detail'),
    path("<int:pk>/edit/", CatUpdateView.as_view(), name="cat_edit"),
    path("<int:pk>/delete/", CatDeleteView.as_view(), name="cat_delete"),
    path("<int:cat_id>/photos/", views.manage_cat_photos, name="manage_cat_photos"),
    path("photos/<int:image_id>/update/", views.update_cat_image, name="update_cat_image"),
    path("photos/<int:image_id>/delete/", views.delete_cat_image, name="delete_cat_image"),
]