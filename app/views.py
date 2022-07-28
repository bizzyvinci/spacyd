from datetime import datetime
import json
import random
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from store.views import get_item, get_items, get_orders, save_purchase
from rapyd.views import confirm_transaction, get_virtual_account


@login_required
def index(request):
  """
  Transfer to store or purchase page
  """
  return render(request, "app/index.html")


@login_required
def store(request):
  """
  Go to store and list items
  """
  items = get_items(request, request.user.country)
  return render(request, "app/store.html", {"items": json.loads(items.content)['data']})


@login_required
def make_payment(request, item_id, currency):
  """
  Provide payment details based on users preferred country and currency
  """
  account = get_virtual_account(request, request.user.get_country_display(), request.user.country)
  item = get_item(request, item_id, request.user.country)
  context = {"item": json.loads(item.content)['data'], "account": json.loads(account.content)["data"]}
  return render(request, "app/pay.html", context)


@login_required
def verify_payment(request):
  """
  ASSUME payment has been made and generate fake receipt,
  Add to purchased items and redirect to orders.
  """
  # currency, amount, virtual_account_id, item_id
  data = request.POST.dict()
  
  new_request = HttpRequest()
  new_request.POST = {
    "receipt_id": ''.join(random.choice(string.ascii_letters) for i in range(10)),
    "item_id": data["item_id"],
    "currency": data["currency"],
    "amount": data["amount"],
    "to_balance": 0,
    "user_id": request.user.username,
    "timestamp": datetime.now()
  }
  save_purchase(new_request)
  messages.success(request, "Payment confirmed")
  return redirect("app:orders")


@login_required
def verify_payment_if_not_virtual(request):
  """
  **UNUSED**
  In a non virtual sandbox. Payment would be verified by name.
  Check if payment has been made and provide receipt,
  and add to purchased items.
  Redirect to orders if successful else pay
  """
  fullname = request.user.get_full_name()
  # currency, amount, virtual_account_id, item_id, 
  data = request.POST.dict()
  item_id = 1
  # Check bank transactions
  transaction = json.loads(confirm_transaction(request, data["virtual_account_id"], fullname).content)['data']
  if not transaction:
    messages.error(request, "Payment not yet made")
    redirect('app:pay', data["item_id"], data["currency"])
  elif transaction["currency"] != data["currency"]:
    messages.error(request, "The right currency was not used. Contact support to proceed with further payments or refund")
  elif transaction["amount"] != data["amount"]:
    messages.error(request, "The right amount was not sent. Contact support to proceed with further payments or refund")
    
  # Store purchase
  new_request = HttpRequest()
  new_request.POST = {
    "receipt_id": transaction["receipt"],
    "item": data["item_id"],
    "currency": transaction["currency"],
    "amount": transaction["amount"],
    "to_balance": data["amount"] - transaction["amount"],
    "user_id": request.user.username,
    "timestamp": datetime.now()
  }
  save_purchase(new_request)
  messages.success(request, "Payment confirmed")
  return redirect("app:orders")


@login_required
def orders(request):
  """
  Show purchased items by user
  """
  orders = get_orders(request, request.user.username)
  context = {"orders": json.loads(orders.content)["data"]}
  return render(request, 'app/orders.html', context)
