from django.urls import path
from .views import PartnerUpdate

urlpatterns = [
    path('import/', PartnerUpdate.as_view(), name='partner-update'),
]


