from django.urls import path
from .views import SupplierListView, SupplierCreateView, ShipmentListView, ShipmentCreateView, home, PalletListView, PalletCreateView, SupplierUpdateView, ShipmentDeleteView, ShipmentUpdateView, SupplierDeleteView


urlpatterns = [
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier_create'),
    path('shipments/', ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/add/', ShipmentCreateView.as_view(), name='shipment_create'),
    path('', home, name='home'),
    path("pallets/", PalletListView.as_view(), name="pallet_list"),
    path("pallets/add/", PalletCreateView.as_view(), name="pallet_create"),
    path("suppliers/edit/<int:pk>/", SupplierUpdateView.as_view(), name="supplier_edit"),
    path("shipments/edit/<int:pk>/", ShipmentUpdateView.as_view(), name="shipment_edit"),
    path("shipments/delete/<int:pk>/", ShipmentDeleteView.as_view(), name="shipment_delete"),
    path("suppliers/delete/<int:pk>/", SupplierDeleteView.as_view(), name="supplier_delete"),
]