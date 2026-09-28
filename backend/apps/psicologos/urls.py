from django.urls import path

from .views import PsicologoDetailView, PsicologoListCreateView

app_name = "psicologos"

urlpatterns = [
    path("", PsicologoListCreateView.as_view(), name="list-create"),
    path("<int:pk>/", PsicologoDetailView.as_view(), name="detail"),
]
