from rest_framework import generics

from apps.access_control.permissions import IsManager

from .models import Psicologo
from .serializers import PsicologoSerializer


class PsicologoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsManager]
    serializer_class = PsicologoSerializer
    queryset = Psicologo.objects.select_related("fila").all()


class PsicologoDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsManager]
    serializer_class = PsicologoSerializer
    http_method_names = ["get", "patch", "head", "options"]
    queryset = Psicologo.objects.select_related("fila").all()
