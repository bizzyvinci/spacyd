from django.http import JsonResponse
from django.shortcuts import render
from .models import Item, Price, Purchase

def get_items(request, currency):
  """
  Get all items in store and price with the specified currency.
  """
  prices = Price.objects.filter(currency=currency)
  items = prices.values('id', 'amount', 'currency', 'item__id', 'item__name', 'item__description')
  items = [{
    'id': x['item__id'],
    'price': x['amount'],
    'currency': x['currency'],
    'name': x['item__name'],
    'description': x['item__description']
  } for x in items]
  return JsonResponse({"data": items})

def get_item(request, item_id, currency):
  """
  Get item with provided id and currency (to know price)
  """
  price = Price.objects.get(item__id=item_id, currency=currency)
  item = {
    'id': price.item.id,
    'price': price.amount,
    'currency': price.currency,
    'name': price.item.name,
    'description': price.item.description
  }
  return JsonResponse({'data': item})

def get_orders(request, user_id):
  """
  Get purchases made by user_id
  """
  purchase = Purchase.objects.filter(user_id=user_id)
  orders = [{
    "name": x.item.name,
    "description": x.item.description,
    "currency": x.currency,
    "amount": x.amount,
    "timestamp": x.timestamp,
  } for x in purchase]
  return JsonResponse({"data": orders})

def save_purchase(request):
  """
  Save a verified purchase
  """
  data = request.POST
  purchase = Purchase(**data)
  purchase.save()
  return JsonResponse({"data": {"success": True}})
