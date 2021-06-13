from rest_framework import fields, serializers
from recipe.models import ShopList

class ShopListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopList
        fields = ('recipe',)