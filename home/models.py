from django.db import models
from django.contrib.auth.models import User
from super_admin.models import Product
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.IntegerField()


class Order(models.Model):
    ORDER_PLACED = 1
    ORDER_CANCELLED = 2
    ORDER_SHIPPED = 3
    ORDER_DELIVERED = 4

    PAYMENT_COD = 1
    PAYMENT_PAYPAL = 2

    ORDER_CHOICES = ((ORDER_PLACED, 'Order placed'), (ORDER_CANCELLED, 'Order cancelled'),
                     (ORDER_SHIPPED, 'Order shipped'), (ORDER_DELIVERED, 'Order delivered'))
    PAYMENT_CHOICES = ((PAYMENT_COD, 'C O D'), (PAYMENT_PAYPAL, 'Paypal'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    tid = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    payment_done = models.BooleanField()
    order_status = models.IntegerField(choices=ORDER_CHOICES)
    payment_mode = models.IntegerField(choices=PAYMENT_CHOICES)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total_price(self):
        return self.product.price * self.quantity
