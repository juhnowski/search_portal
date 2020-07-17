from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import JournalRecord


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalRecord
        fields = '__all__'
