from rest_framework import serializers
from produto.models import Produtos

class ProdutosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'