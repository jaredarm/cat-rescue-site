from django.urls import path
from .views import PageDetailView, PageEditView

urlpatterns = [
    path('<slug:slug>/', PageDetailView.as_view(), name='page_detail'),
     path("<slug:slug>/edit/", PageEditView.as_view(), name="page_edit"),
]