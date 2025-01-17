from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from yaml import load, Loader
from requests import get
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class PartnerUpdate(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                try:
                    data = load(stream, Loader=Loader)
                except Exception as e:
                    return JsonResponse({'Status': False, 'Error': 'Ошибка при чтении данных из файла'})

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)


                ProductInfo.objects.filter(shop_id=shop.id).delete()

                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()

                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(
                        product_id=product.id,
                        shop_id=shop.id,
                        quantity=item.get('quantity', 0),
                        price=item.get('price', 0.0),
                        price_rrc=item.get('price_rrc', 0.0)
                    )

                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(
                            product_info_id=product_info.id,
                            parameter_id=parameter_object.id,
                            value=value
                        )

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})




