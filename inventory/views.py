import requests
from datetime import date

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from .models import InventoryItem
from .forms import InventoryItemForm


def item_list(request):
    # ---------- アイテム登録 ----------
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_list')
    else:
        form = InventoryItemForm()

    # ---------- 在庫一覧 ----------
    items = InventoryItem.objects.all().order_by("-id")
    today = date.today()
    for item in items:
        if item.expiration_date:
            delta_days = (item.expiration_date - today).days
            item.days_left = delta_days
        else:
            item.days_left = None

    # ---------- Spoonacular レシピ検索 ----------
    keyword = request.GET.get("q", "")
    recipes = []

    if keyword:
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": settings.SPOONACULAR_API_KEY,
            "query": keyword,
            "number": 10,  # 最大件数
        }

        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            for r in data.get("results", []):
                recipes.append({
                    "title": r.get("title"),
                    "id": r.get("id"),  
                    "image": r.get("image"),
                })

    context = {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    }

    return render(request, "inventory/item_list.html", context)


def recipe_detail(request, recipe_id):
    """
    Spoonacular API からレシピ詳細を取得して表示する
    """
    recipe = None
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": settings.SPOONACULAR_API_KEY}

    res = requests.get(url, params=params)
    if res.status_code == 200:
        recipe = res.json()

    return render(request, "inventory/recipe_detail.html", {"recipe": recipe})


def item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})


def item_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "inventory/item_edit.html", {"form": form})
