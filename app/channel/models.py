from django.db import models

from app.catalog.models import Product
from app.core.mixins import ModelsMixin

# Create your models here.


class Channel(ModelsMixin):
    name = models.CharField()
    description = models.CharField(null=True)

    def __str__(self):
        return self.name


class ChannelPrice(ModelsMixin):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="channel_price"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_price"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = [["channel", "product"]]

    def __str__(self):
        return self.price
