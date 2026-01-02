from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem
from .forms import InventoryItemForm
from datetime import date

def item_list(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
    else:
        form = InventoryItemForm()

    items = InventoryItem.objects.all()
    today = date.today()
    for item in items:
        delta = (item.expiration_date - today).days
        if delta < 0:
            item.color = 'brown'
        elif delta == 0 or delta == 1:
            item.color = 'red'
        elif delta == 2:
            item.color = 'orange'
        elif 2 < delta <= 5:
            item.color = 'green'
        else:
            item.color = ''

    return render(request, 'inventory/item_list.html', {'items': items, 'form': form})

def item_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/item_edit.html', {'form': form, 'item': item})

def item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    item.delete()
    return redirect('inventory:item_list')