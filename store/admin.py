from django.contrib import admin
from .models import Item, Price, Purchase

# Register your models here.
admin.site.register([Item, Price, Purchase])
