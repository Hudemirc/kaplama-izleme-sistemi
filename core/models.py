from django.db import models
from django.contrib.auth.models import User


class WoodType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_suppliers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_suppliers")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Shipment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="shipments", verbose_name="Tedarikçi")
    date = models.DateField(verbose_name="Tarih")
    note = models.TextField(blank=True, null=True, verbose_name="Açıklama")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_shipments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_shipments")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sevkiyat-{self.supplier.name} {self.date}"
    
class SupplierQualityType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class LengthGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    nominal_length = models.FloatField(help_text="Hesaplama için nominal uzunluk (cm)")
    is_dynamic_length = models.BooleanField(default=False, help_text="Kısa parça mı?")

    def __str__(self):
        return self.name
    
class Pallet(models.Model):
    shipment = models.ForeignKey("Shipment", on_delete=models.CASCADE, related_name="pallets")
    wood_type = models.ForeignKey(WoodType, on_delete=models.CASCADE)
    supplier_quality_type = models.ForeignKey("SupplierQualityType", on_delete=models.SET_NULL, null=True, blank=True)
    length_group = models.ForeignKey("LengthGroup", on_delete=models.SET_NULL, null=True, blank=True)

    barcode = models.CharField(max_length=100, unique=True)
    total_area = models.FloatField(help_text="Tedarikçinin verdiği toplam m²")

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)

    total_vat = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price_with_vat = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_pallets")
    created_at = models.DateTimeField(auto_now_add=True)
    inspected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="inspected_pallets")
    inspected_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_pallets")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = f"PAL-{self.pk or 'TEMP'}"
        self.total_price = self.total_area * float(self.unit_price)
        self.total_vat = self.total_price * float(self.vat_rate) / 100
        self.total_price_with_vat = self.total_price + self.total_vat
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pallet #{self.id} - {self.wood_type.name}"