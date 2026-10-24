from rest_framework import serializers

from products.models import Category, Order, Products


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


class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(),
        many=True,
        allow_empty=False,
    )

    class Meta:
        model = Order
        fields = (
            'payment',
            'email',
            'phone',
            'address',
            'total',
            'items'
        )

    def validate_items(self, value):
        ids = [item.id for item in value]

        # Проверка на дубликаты id
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                'В заказе присутствуют повторяющиеся товары.'
            )

        for item in value:
            if item.price is None:
                raise serializers.ValidationError(
                    f'Товар "{item.title}" недоступен для покупки.'
                )

        return value

    def validate(self, attrs):
        """Проверка суммы заказа"""
        items = attrs['items']
        total = attrs['total']
        calculate_total = sum(item.price for item in items)
        if total != calculate_total:
            raise serializers.ValidationError({
                'total': 'Неверная стоимость заказа.'
            })
        return attrs


class OrderResponseSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(read_only=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'total'
        )

class OderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'number',
            'id',
            'payment',
            'email',
            'phone',
            'address',
            'total',
            'items',
            'created_at'
        )
