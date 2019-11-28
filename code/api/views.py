from rest_framework import viewsets

from api.serializers import RawEntitySerializer
from info.models import RawEntity


class RawEntityViewSet(viewsets.ModelViewSet):
    queryset = RawEntity.objects.all()
    serializer_class = RawEntitySerializer
