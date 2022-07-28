from django.contrib import admin
from .models import VirtualAccount, Transaction

# Register your models here.
admin.site.register([VirtualAccount, Transaction])
