from django.db import models


class ModelsMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted = models.DateTimeField(default=None, blank=True, null=True)
