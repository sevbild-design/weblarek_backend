from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.serializers import ProductSerializer
from products.models import Products


class ProductsListViewSet(ListAPIView):
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
