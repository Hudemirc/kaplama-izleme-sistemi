from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Supplier, Shipment, Pallet
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required
def home(request):
    return render(request, "core/home.html")


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = "core/supplier_list.html"
    context_object_name = "suppliers"

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    fields = ['name', 'country', 'phone', 'email', 'note']
    template_name = "core/supplier_form.html"
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = "core/shipment_list.html"
    context_object_name = "shipments"
    ordering = ['-id']  # Varsayılan sıralama

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtreleme işlemi
        supplier = self.request.GET.get('supplier')
        date = self.request.GET.get('date')
        is_filled = self.request.GET.get('is_filled')

        if supplier:
            queryset = queryset.filter(supplier__name__icontains=supplier)
        
        if date:
            queryset = queryset.filter(date=date)
        
        if is_filled:
            queryset = queryset.filter(is_filled=is_filled)
        
        # is_filled True olanları sona alacak şekilde sıralama
        queryset = queryset.order_by('is_filled', '-id')

        return queryset

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['supplier', 'date', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "core/shipment_form.html"
    success_url = reverse_lazy('shipment_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
class ShipmentDetailView(DetailView):
    model = Shipment
    template_name = 'core/shipment_detail.html'
    context_object_name = 'shipment'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pallets'] = self.object.pallets.all()  # Sevkiyata bağlı paletler
        return context
    
class PalletListView(LoginRequiredMixin, ListView):
    model = Pallet
    template_name = "core/pallet_list.html"
    context_object_name = "pallets"
    ordering = ['-id']

class PalletCreateView(LoginRequiredMixin, CreateView):
    model = Pallet
    fields = [
        "shipment",
        "wood_type",
        "supplier_quality_type",
        "length_group",
        "total_area",
        "unit_price",
        "currency",
        "vat_rate",
    ]
    template_name = "core/pallet_form.html"
    success_url = reverse_lazy("pallet_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
class PalletUpdateView(UpdateView):
    model = Pallet
    fields = ['unit_price', 'total_area']  # Ekleme / Güncelleme yapmak istediğimiz alanlar
    template_name = 'core/pallet_form.html'
    success_url = reverse_lazy('pallet_list')  # Güncelleme sonrası listeye dön
    
    def get_object(self):
        return get_object_or_404(Pallet, pk=self.kwargs['pk'])
    
class PalletDeleteView(DeleteView):
    model = Pallet
    template_name = 'core/pallet_confirm_delete.html'
    success_url = reverse_lazy('pallet_list')
    


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    fields = ["name", "phone", "email", "country", "note"]
    template_name = "core/supplier_form.html"
    success_url = reverse_lazy("supplier_list")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class ShipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Shipment
    fields = ["supplier", "date", "is_filled", "note"]
    template_name = "core/shipment_form.html"
    success_url = reverse_lazy("shipment_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Sevkiyat Düzenle: {self.object.supplier.name} - {self.object.date}"
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        # `is_filled`'ı True yapıyoruz
        if 'is_filled' in form.cleaned_data:
            form.instance.is_filled = form.cleaned_data['is_filled']
        return super().form_valid(form)
    
class ShipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Shipment
    template_name = "core/shipment_confirm_delete.html"
    success_url = reverse_lazy("shipment_list")

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = "core/supplier_confirm_delete.html"
    success_url = reverse_lazy("supplier_list")

    def dispatch(self, request, *args, **kwargs):
        supplier = self.get_object()
        if supplier.shipments.exists():
            from django.contrib import messages
            messages.error(request, "Bu tedarikçiye ait sevkiyatlar var, silemezsiniz.")
            return redirect("supplier_list")
        return super().dispatch(request, *args, **kwargs)