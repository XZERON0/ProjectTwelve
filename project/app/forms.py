from django import forms
from . import models
class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'category', 'unit']
class SupplierForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = ['name', 'phone']
class IncomeForm(forms.ModelForm):
    class Meta:
        model = models.Income
        fields = ['product', 'supplier', 'quantity', 'price', 'total_sum', 'accepted_by', 'date']
class SaleForm(forms.ModelForm):
    class Meta:
        model = models.Sale
        fields = ['user', 'total_sum', 'created_at']
