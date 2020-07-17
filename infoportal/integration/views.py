from rest_framework import generics, filters

from .models import JournalRecord
from .serializers import JournalSerializer
from users.utils.permissions import *


class JournalApiView(generics.ListAPIView):
    """
    Возвращает журнал импорта. Умеет фильтровать записи по типу.
    """
    permission_classes = (IsAdmin,)
    serializer_class = JournalSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-timestamp']

    def get_queryset(self):
        record_type = self.request.query_params.get('type')
        if record_type is None:
            return JournalRecord.objects.all()
        else:
            return JournalRecord.objects.filter(type=record_type)
