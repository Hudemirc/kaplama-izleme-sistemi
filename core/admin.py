from django.contrib import admin
from .models import WoodType, Supplier, Shipment

@admin.register(WoodType)
class WoodTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'created_by', 'created_at']
    search_fields = ['name', 'phone', 'email']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'date', 'created_by', 'created_at']
    search_fields = ['supplier__name', 'note']