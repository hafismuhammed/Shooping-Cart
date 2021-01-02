from django.db import models
from django.contrib.auth.models import User
from adminpanel.models import Product


class CusetomerCart(models.Model):
    customer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username

