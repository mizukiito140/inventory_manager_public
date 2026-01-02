from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem
from .forms import InventoryItemForm

# 一覧
def item_list(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
    else:
        form = InventoryItemForm()

    items = InventoryItem.objects.all()

    return render(
        request,
        'inventory/item_list.html',
        {
            'form': form,
            'items': items
        }
    )
# 削除処理
def item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        item.delete()
    return redirect('inventory:item_list')
    
#編集処理
def item_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
    else:
        form = InventoryItemForm(instance=item)

    return render(request, 'inventory/item_edit.html', {'form': form})