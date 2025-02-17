# serializers.py

from rest_framework import serializers

class PrevisaoSerializer(serializers.Serializer):
    data = serializers.DateField()
    saldo_previsto = serializers.FloatField()
