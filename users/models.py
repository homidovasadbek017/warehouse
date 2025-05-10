from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Branch


class User(AbstractUser):
    phone = models.CharField(max_length=13)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    # image = models.ImageField(upload_to='media/images/')
