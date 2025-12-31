# items/forms.py
from django import forms
from .models import InventoryItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["name", "expiration_date"]
        labels = {
            "name": "アイテム名",
            "expiration_date": "期限",
        }