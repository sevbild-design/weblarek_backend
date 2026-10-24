from django.db import transaction
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import (OderListSerializer, OrderCreateSerializer,
                             OrderResponseSerializer, ProductSerializer)
from products.models import Order, Products


class ProductsViewSet(
     ListModelMixin, GenericViewSet
):
    serializer_class = ProductSerializer
    queryset = Products.objects.select_related(
        'category'
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'total': queryset.count(),
            'items': serializer.data,
        })

class OrderViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet):
    queryset=Order.objects.prefetch_related('items')
    serializer_class = OrderCreateSerializer

    # Если одна из операций завершится ошибкой,
    # Django отменит все изменения, сделанные в рамках этой транзакции.
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Меняем сериализатор ответа сервера"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response_serializer = OrderResponseSerializer(order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = OderListSerializer(queryset, many=True)
    
            return Response({
                'total': queryset.count(),
                'orders': serializer.data,
            })



