from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image_url = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)

