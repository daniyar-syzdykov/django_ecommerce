from django.urls import path

from .views import test_view, products, product_by_id

urlpatterns = [
    path('', products, name='get_all_products'),
    path('<int:id>', product_by_id, name='get_product_by_id'),
]
