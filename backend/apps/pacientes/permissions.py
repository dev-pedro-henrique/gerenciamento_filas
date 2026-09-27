from rest_framework.permissions import BasePermission

from apps.access_control.models import User


class IsPatientStaff(BasePermission):
    message = "Você não tem permissão para acessar os pacientes."

    def has_permission(self, request, view):
        del view

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.role
            in {
                User.Role.MANAGER,
                User.Role.RECEPTIONIST,
            }
        )