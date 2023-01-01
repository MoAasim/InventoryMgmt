from django.forms import ModelForm
from django import forms
from .models import Inventory


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']
    
    def clean(self):
        super().clean()
        stock = int(self.cleaned_data.get('quantity_in_stock'))
        sold = int(self.cleaned_data.get('quantity_sold'))
        cost = float(self.cleaned_data.get('cost_per_item'))

        if stock < 0 or sold < 0 or cost < 0:
            raise forms.ValidationError('Cost per item OR stock quantity OR quantity sold should not be NEGATIVE')

        if sold > stock:
            raise forms.ValidationError('Quantity sold should be less than quantity in stock')

        return self.cleaned_data
