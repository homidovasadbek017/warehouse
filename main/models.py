from django.core.validators import MinValueValidator
from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BaseModel(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    import_price = models.FloatField(validators=[MinValueValidator(0.0)])
    export_price = models.FloatField(validators=[MinValueValidator(0.0)], null=True)
    amount = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Client(BaseModel):
    name = models.CharField(max_length=255)
    market = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    address = models.TextField()
    debt = models.FloatField(validators=[MinValueValidator(0.0)], default=0)

    def __str__(self):
        return self.name



