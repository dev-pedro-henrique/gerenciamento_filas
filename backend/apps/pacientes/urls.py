from django.urls import path

from .views import (
    PacienteBuscarView,
    PacienteCreateView,
    PacienteDetailView,
)


app_name = "pacientes"

urlpatterns = [
    path("", PacienteCreateView.as_view(), name="create"),
    path("buscar/", PacienteBuscarView.as_view(), name="buscar"),
    path("<int:pk>/", PacienteDetailView.as_view(), name="detail"),
]