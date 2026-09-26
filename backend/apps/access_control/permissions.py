from rest_framework.permissions import BasePermission

from .models import User


class IsManager(BasePermission):
    message = "Apenas o gestor pode realizar esta operação."

    def has_permission(self, request, view) -> bool:
        del view
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.MANAGER
            and request.user.is_active
        )
