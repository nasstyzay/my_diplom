from rest_framework import serializers
from .models import Shop, Category, Product, ProductInfo, Order, OrderItem, Contact, Parameter, ProductParameter


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'shops']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'name']


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductInfo
        fields = ['product', 'shop', 'quantity', 'price', 'price_rrc']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'dt', 'status']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'shop', 'quantity']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['user', 'type', 'value']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name']


class ProductParameterSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer()
    parameter = ParameterSerializer()

    class Meta:
        model = ProductParameter
        fields = ['product_info', 'parameter', 'value']
