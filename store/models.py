from locale import currency
from django.db import models

class Item(models.Model):
  """
  Model for item details
  """
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=1000)
  
  def __str__(self) -> str:
    return self.name

class Price(models.Model):
  """
  Model for item price
  """
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  #currency = models.TextChoices('USD', 'SGD')
  currency = models.CharField(max_length=3)
  amount = models.IntegerField()
  
  def __str__(self) -> str:
    return f"{self.item}: {self.amount} {self.currency}"

class Purchase(models.Model):
  """
  Model for purchases made (aka fulfilled orders)
  """
  receipt_id = models.CharField(max_length=12)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  currency = models.CharField(max_length=3)
  amount = models.IntegerField()
  to_balance = models.IntegerField()
  user_id = models.CharField(max_length=50)
  timestamp = models.DateTimeField()
