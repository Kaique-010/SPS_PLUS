from rest_framework import serializers
from .models import PedidoVenda
from decimal import Decimal, InvalidOperation

class PedidoVendaSerializer(serializers.ModelSerializer):
    valor_total = serializers.DecimalField(source='pedi_tota', max_digits=15, decimal_places=15, read_only=True)

    class Meta:
        model = PedidoVenda
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            # Verificar e corrigir valores inválidos aqui
            Decimal(representation['valor_total'])
        except InvalidOperation:
            representation['valor_total'] = 'Valor inválido'
        return representation