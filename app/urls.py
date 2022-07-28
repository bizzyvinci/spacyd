from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
  path("", views.index, name="index"),
  path("store/", views.store, name="store"),
  path("orders/", views.orders, name="orders"),
  path("pay/<int:item_id>/<str:currency>/", views.make_payment, name="pay"),
  path("paid/", views.verify_payment, name="paid"),
]
