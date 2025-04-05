from django.contrib import admin
from .models import WoodType, Supplier, Shipment, SupplierQualityType, LengthGroup, Pallet

admin.site.register(WoodType)

admin.site.register(SupplierQualityType)

admin.site.register(LengthGroup)

admin.site.register(Pallet)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'created_by', 'created_at']
    search_fields = ['name', 'phone', 'email']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'date', 'created_by', 'created_at']
    search_fields = ['supplier__name', 'note']

