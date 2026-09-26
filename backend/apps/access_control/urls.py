from django.urls import path

from .views import (
    CsrfTokenView,
    CurrentUserView,
    LoginView,
    LogoutView,
    ReceptionistDetailView,
    ReceptionistListCreateView,
    ReceptionistPasswordResetView,
)

app_name = "access_control"
urlpatterns = [
    path("auth/csrf/", CsrfTokenView.as_view(), name="csrf"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", CurrentUserView.as_view(), name="current-user"),
    path("staff/receptionists/", ReceptionistListCreateView.as_view(), name="receptionists"),
    path(
        "staff/receptionists/<int:pk>/",
        ReceptionistDetailView.as_view(),
        name="receptionist-detail",
    ),
    path(
        "staff/receptionists/<int:pk>/reset-password/",
        ReceptionistPasswordResetView.as_view(),
        name="receptionist-reset-password",
    ),
]
