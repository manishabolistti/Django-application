from django import forms
from .models import Bill, Stock, Item

# Form for customer details in the bill
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name', 'customer_phone']
        labels = {
            'customer_name': 'Customer Name',
            'customer_phone': 'Customer Phone',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BillItemForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control category-select'}),
        label="Category Type"
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.none(),  # Initially empty
        widget=forms.Select(attrs={'class': 'form-control item-select'}),
        label="Item Name"
    )
    quantity = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Quantity"
    )
    rate = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Rate per Unit"
    )

    def __init__(self, *args, **kwargs):
        # Dynamically populate the item queryset for each form in the formset
        data = kwargs.get('data')
        super().__init__(*args, **kwargs)
        if data:
            category_id = data.get(self.add_prefix('category'))
            if category_id:
                try:
                    self.fields['item'].queryset = Item.objects.filter(stock_id=category_id)
                except (ValueError, TypeError):
                    self.fields['item'].queryset = Item.objects.none()