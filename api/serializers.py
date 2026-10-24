from rest_framework import serializers

from products.models import Category, Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'id',
            'description',
            'image',
            'title',
            'category',
            'price'
        )

