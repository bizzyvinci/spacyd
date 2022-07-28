from datetime import datetime, timedelta
import time
from django.http import JsonResponse
from django.shortcuts import render
from .models import VirtualAccount, Transaction


def get_virtual_account(request, country, currency):
  """Get account details for country and currency"""
  account = {
    "bank": "ABC Bank",
    "number": "123456789",
    "name": "Spacyd",
  }
  account = VirtualAccount.objects.get(currency=currency, country=country)
  data = {
    "id": account.account_id,
    "type": account.account_type,
    "bank": account.bank,
    "number": account.number,
    "name": account.name,
    "country": account.country,
    "currency": account.currency,
  }
  return JsonResponse({"data": data})


def confirm_transaction(request, account_id, fullname):
  """
  Confirm that a new deposit was made.
  New deposits are less than 6 hours (to reduce fraud) and not used/confirmed before
  """
  transaction = Transaction.objects.get(account_id=account_id, recipient=fullname, confirmed=False, timestamp=datetime.now() - timedelta(hours=6))
  if transaction is not None:
    transaction.confirmed = True
    transaction.save()
  data = {
    "amount": transaction.amount,
    "currency": transaction.account.currency,
    "timestamp": transaction.timestamp,
    "receipt": transaction.receipt,
  }
  return JsonResponse({"data": data})


def handle_deposit_webhook(request):
  """
  Handle webhook for deposits and save to Transaction model.
  """
  pass


def make_refund(request, details):
  """
  Make refund to a user
  """
  pass
