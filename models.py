from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.URLField(verbose_name='URL')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    shops = models.ManyToManyField(Shop, related_name='categories', verbose_name='Магазины')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_infos', verbose_name='Продукт')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='product_infos', verbose_name='Магазин')
    name = models.CharField(max_length=255, verbose_name='Название')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Рекомендованная розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информация о продуктах'

    def __str__(self):
        return f"{self.product.name} в {self.shop.name}"

class Parameter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, related_name='product_parameters', verbose_name='Информация о продукте')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='product_parameters', verbose_name='Параметр')
    value = models.CharField(max_length=255, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'

    def __str__(self):
        return f"{self.parameter.name}: {self.value}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.CharField(max_length=50, choices=[('new', 'Новый'), ('in_progress', 'В процессе'),
                                                      ('completed', 'Завершён'), ('cancelled', 'Отменён')], verbose_name='Статус')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-dt',)

    def __str__(self):
        return f"Заказ {self.id} от {self.dt} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Продукт')

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='order_items', verbose_name='Магазин')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Contact(models.Model):
    CONTACT_TYPES = (('phone', 'Телефон'), ('email', 'Email'), ('address', 'Адрес'))
    type = models.CharField(max_length=50, choices=CONTACT_TYPES, verbose_name='Тип')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', verbose_name='Пользователь')
    value = models.CharField(max_length=255, verbose_name='Значение')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.get_type_display()}: {self.value}"
