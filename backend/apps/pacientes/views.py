from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paciente
from .permissions import IsPatientStaff
from .serializers import CPFSerializer, PacienteSerializer


class PacienteCreateView(generics.CreateAPIView):
    permission_classes = [IsPatientStaff]
    serializer_class = PacienteSerializer


class PacienteBuscarView(APIView):
    permission_classes = [IsPatientStaff]

    def post(self, request):
        serializer = CPFSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        paciente = Paciente.objects.filter(
            cpf=serializer.validated_data["cpf"]
        ).first()

        if not paciente:
            return Response(
                {"detail": "Nenhum paciente encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            PacienteSerializer(paciente).data,
            status=status.HTTP_200_OK,
        )


class PacienteDetailView(generics.RetrieveAPIView):
    permission_classes = [IsPatientStaff]
    serializer_class = PacienteSerializer
    queryset = Paciente.objects.all()