from django.urls import path
from .views import ApplicationCreateView, ApplicationListView, ApplicationDetailView

urlpatterns = [
    path('', ApplicationListView.as_view(), name='application_list'),
    path('add/', ApplicationCreateView.as_view(), name='application_add'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    # path("<int:pk>/edit/", ApplicationUpdateView.as_view(), name="application_edit"),
    # path("<int:pk>/delete/", ApplicationDeleteView.as_view(), name="application_delete"),
]