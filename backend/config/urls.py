from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.access_control.urls")),
    path("api/pacientes/", include("apps.pacientes.urls")),
]