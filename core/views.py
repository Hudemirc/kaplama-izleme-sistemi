from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Supplier, Shipment
from django import forms
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "core/home.html")


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = "core/supplier_list.html"
    context_object_name = "suppliers"

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    fields = ['name', 'phone', 'email', 'note']
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