import requests
from datetime import date

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from .models import InventoryItem
from .forms import InventoryItemForm


# -----------------------------
# 内部ヘルパー
# -----------------------------
def _handle_item_create(request):
    """
    アイテム登録（POST時）を処理する。
    成功したら redirect を返し、失敗/GETなら form を返す。
    """
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list"), None
        return None, form  # バリデーションエラー時は form を返す

    # GET のとき（初期表示）
    return None, InventoryItemForm()


def _get_items_with_days_left():
    """
    アイテム一覧を取得し、各 item に days_left を付与する。
    """
    items = InventoryItem.objects.all().order_by("-id")
    today = date.today()

    for item in items:
        if item.expiration_date:
            item.days_left = (item.expiration_date - today).days
        else:
            item.days_left = None

    return items


def _search_recipes(keyword):
    """
    Spoonacular でレシピ検索し、表示用に必要な最低限の情報へ整形して返す。
    """
    if not keyword:
        return []

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": settings.SPOONACULAR_API_KEY,
        "query": keyword,
        "number": 10,
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException:
        return []

    recipes = []
    for r in data.get("results", []):
        recipes.append({
            "title": r.get("title"),
            "id": r.get("id"),
            "image": r.get("image"),
        })
    return recipes


def _fetch_recipe_detail(recipe_id):
    """
    Spoonacular からレシピ詳細を取得して dict を返す。失敗したら None。
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": settings.SPOONACULAR_API_KEY}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException:
        return None


# -----------------------------
# ビュー（外から呼ばれる関数）
# -----------------------------
def item_list(request):
    # 1) アイテム登録
    redirect_response, form = _handle_item_create(request)
    if redirect_response:
        return redirect_response

    # 2) アイテム一覧 + 色分け用 days_left 付与
    items = _get_items_with_days_left()

    # 3）レシピ検索（GET）
    keyword = request.GET.get("q", "").strip()
    recipes = _search_recipes(keyword)

    context = {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    }
    return render(request, "inventory/item_list.html", context)


def recipe_detail(request, recipe_id):
    recipe = _fetch_recipe_detail(recipe_id)
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
