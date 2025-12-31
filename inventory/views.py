from django.shortcuts import render
from .models import InventoryItem

def item_list(request):
    items = InventoryItem.objects.all().order_by("expiration_date")
    return render(request, "inventory/item_list.html", {
        "items": items
    })