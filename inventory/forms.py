# items/forms.py
from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["name", "expiration_date"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "アイテム名"
            }),
            "expiration_date": forms.DateInput(attrs={
                "type": "date"
            }),
        }