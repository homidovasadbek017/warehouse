from main.models import *
from django.db import models


class Sale(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField(default=1)
    sold_at = models.DateTimeField()

    total_price = models.FloatField()
    paid_price = models.FloatField()
    debt_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.client.name}"


class Import(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField(default=1)
    total_price = models.FloatField()
    per_price = models.FloatField()
    deliverer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product.name} {self.amount} {self.product.unit}'

