from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        "User", blank=True, null=True, on_delete=models.SET_NULL
    )
    email = models.EmailField(max_length=50, unique=True)
