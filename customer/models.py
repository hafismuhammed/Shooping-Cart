from django.db import models
from django.contrib.auth.models import User
from adminpanel.models import Product


class CusetomerCart(models.Model):
    customer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username

class Checkout(models.Model):
    customer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=255)
    payment_id = models.CharField(max_length=255, null=True, default=None)
    total_amount = models.FloatField()
    payment_singnature = models.CharField(max_length=255, null=True, default=None)
    reciept_num = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=2000)
    delivery_phoone = models.CharField(max_length=20)
    payment_completed = models.BooleanField()
    payment_date = models.DateTimeField(auto_now_add=True)

class CustomerPayedProduct(models.Model):
    customer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    checkout_details = models.ForeignKey(Checkout, null=False, blank=False, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    product_description = models.CharField(max_length=2000)
    