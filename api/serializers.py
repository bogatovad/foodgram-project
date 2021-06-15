from rest_framework import serializers
from recipe.models import ShopList


class ShopListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopList
        fields = ('recipe',)
