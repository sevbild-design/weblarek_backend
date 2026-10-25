from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import OrderViewSet, ProductsViewSet

router_v1 = DefaultRouter()
router_v1.register(
    'order',
    OrderViewSet,
    basename='order'
    )

router_v1.register(
    'product',
    ProductsViewSet,
    basename='product'
    )

urlpatterns = [
    path('weblarek/', include(router_v1.urls)),
]
