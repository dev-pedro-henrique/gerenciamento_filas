from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsManager
from .serializers import (
    CurrentUserSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    ReceptionistSerializer,
    ReceptionistUpdateSerializer,
)
from .services import (
    authenticate_user,
    end_current_session,
    start_single_session,
    terminate_user_session,
)


class CsrfTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate_user(request=request, **serializer.validated_data)
        start_single_session(request, user)
        return Response(CurrentUserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        end_current_session(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    def get(self, request):
        return Response(CurrentUserSerializer(request.user).data)


class ReceptionistListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = ReceptionistSerializer

    def get_queryset(self):
        return User.objects.filter(role=User.Role.RECEPTIONIST)


class ReceptionistDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsManager]
    serializer_class = ReceptionistUpdateSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return User.objects.filter(role=User.Role.RECEPTIONIST)


class ReceptionistPasswordResetView(generics.GenericAPIView):
    permission_classes = [IsManager]
    serializer_class = PasswordResetSerializer

    def get_queryset(self):
        return User.objects.filter(role=User.Role.RECEPTIONIST)

    def post(self, request, *args, **kwargs):
        receptionist = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receptionist.set_password(serializer.validated_data["password"])
        receptionist.save(update_fields=["password"])
        terminate_user_session(receptionist)
        return Response(status=status.HTTP_204_NO_CONTENT)
