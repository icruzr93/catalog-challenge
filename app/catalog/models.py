from django.db import models

from .mixins import CatalogMixin


class Brand(CatalogMixin):
    name = models.CharField()
    description = models.CharField()

    def __str__(self):
        return self.name


class Product(CatalogMixin):
    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="product_brand"
    )

    def __str__(self):
        return self.name
