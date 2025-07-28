from django.contrib import admin
from .models import Client, Warehouse, StorageUnit
# Register your models here.
admin.site.register(Client)
admin.site.register(Warehouse)
admin.site.register(StorageUnit)
