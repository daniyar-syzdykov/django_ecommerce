import uuid
from datetime import datetime
from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4)
    wish_list = models.ManyToManyField(
        'store.Product', related_name='customer_whish_list')
    cart = models.ManyToManyField(
        'store.Product', related_name='customer_cart')


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    deliverd_at = models.DateField(default=datetime.now())
