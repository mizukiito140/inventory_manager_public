from django.shortcuts import render, redirect
from .models import InventoryItem
from .forms import InventoryItemForm

def item_list(request):
    # フォーム送信時（登録）
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm()

    # 一覧取得
    items = InventoryItem.objects.all().order_by("expiration_date")

    return render(request, "inventory/item_list.html", {
        "form": form,
        "items": items,
    })