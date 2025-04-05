from django.urls import path
from .views import SupplierListView, SupplierCreateView, ShipmentListView, ShipmentCreateView, home

urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier_create'),
    path('shipments/', ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/add/', ShipmentCreateView.as_view(), name='shipment_create'),
    path('', home, name='home'),
]