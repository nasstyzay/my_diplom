from django.urls import include, path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, CategoryViewSet, ProductViewSet, ProductInfoViewSet, OrderViewSet, OrderItemViewSet, ContactViewSet, ParameterViewSet, ProductParameterViewSet

router = DefaultRouter()
router.register(r'shops', ShopViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'productinfo', ProductInfoViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'parameters', ParameterViewSet)
router.register(r'productparameters', ProductParameterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]





