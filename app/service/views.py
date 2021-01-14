from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.service.models import Program
from app.service.serializers import ApplicationCreateSerializer


class ProgramViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin,
):
    permission_classes = (AllowAny,)
    queryset = Program.objects.all()
    serializer_class = ApplicationCreateSerializer

    @action(methods=['post'], detail=False)
    def applicate(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)
