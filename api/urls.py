from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ProductsListViewSet

# router_v1 = DefaultRouter()
# router_v1.register(
#     'product',
#     ProductsListViewSet,
#     basename='product'
#     )

urlpatterns = [
    path('weblarek/product/', ProductsListViewSet.as_view(), name='product'),
]
