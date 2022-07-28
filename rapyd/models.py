from django.db import models

class VirtualAccount(models.Model):
  account_id = models.CharField(max_length=20, primary_key=True)
  account_type = models.CharField(max_length=20)
  bank = models.CharField(max_length=100)
  number = models.CharField(max_length=20)
  name = models.CharField(max_length=100)
  country = models.CharField(max_length=2)
  #an account can handle multiple currencies
  currency = models.CharField(max_length=3)

class Transaction(models.Model):
  account = models.ForeignKey(VirtualAccount, on_delete=models.CASCADE)
  amount = models.IntegerField() # positive for deposits and negative for withdrawals
  recipient = models.CharField(max_length=200)
  confirmed = models.BooleanField() # receipt or refund has been issued for the transaction
  timestamp = models.DateTimeField()
  receipt = models.CharField(max_length=100)
