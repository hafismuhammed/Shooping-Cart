from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.FloatField()
    product_discription = models.CharField(max_length=1000)
    product_picture = models.FileField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name