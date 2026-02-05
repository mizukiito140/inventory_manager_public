# inventory/views.py
import requests
from datetime import date
from typing import List, Dict, Optional, Tuple

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import InventoryItem
from .forms import InventoryItemForm


# =========================
# Public Views (URLに直結)
# =========================

@require_http_methods(["GET", "POST"])
def item_list(request: HttpRequest) -> HttpResponse:
    """
    在庫一覧ページ（同一URLで、登録・一覧・レシピ検索を提供）
    - POST: アイテム登録
    - GET : 一覧表示 + (qがあれば) レシピ検索
    """
    # 1) 登録（POST）の処理：成功ならredirect、失敗ならエラー付きformで継続
    form, redirected = _handle_item_create(request)
    if redirected is not None:
        return redirected

    # 2) 一覧表示データ
    items = _get_items_with_days_left()

    # 3) レシピ検索データ（q がある時だけ外部APIを呼ぶ）
    keyword = request.GET.get("q", "").strip()
    recipes = _search_recipes_if_needed(keyword)

    context = {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    }
    return render(request, "inventory/item_list.html", context)


def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Spoonacular API からレシピ詳細を取得して表示する"""
    recipe = _fetch_recipe_detail(recipe_id)
    return render(request, "inventory/recipe_detail.html", {"recipe": recipe})


def item_delete(request: HttpRequest, pk: int) -> HttpResponse:
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})


def item_edit(request: HttpRequest, pk: int) -> HttpResponse:
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "inventory/item_edit.html", {"form": form})


# =========================
# Helpers (viewsの内部部品)
# =========================

def _handle_item_create(request: HttpRequest) -> Tuple[InventoryItemForm, Optional[HttpResponse]]:
    """
    POSTならアイテム登録を試みる。
    - 成功: (form, redirect_response) を返す
    - 失敗: (error付きform, None) を返す（同ページ再描画用）
    - GET : (空form, None)
    """
    if request.method != "POST":
        return InventoryItemForm(), None

    form = InventoryItemForm(request.POST)
    if form.is_valid():
        form.save()
        return form, redirect("inventory:item_list")

    # バリデーションエラー時は、エラー入りformを返す
    return form, None


def _get_items_with_days_left() -> List[InventoryItem]:
    """一覧表示用に items を取得し、days_left を動的に付与して返す"""
    items = list(InventoryItem.objects.all().order_by("-id"))
    today = date.today()

    for item in items:
        if item.expiration_date:
            item.days_left = (item.expiration_date - today).days
        else:
            item.days_left = None

    return items


def _search_recipes_if_needed(keyword: str) -> List[Dict]:
    """keyword が空なら検索しない。空でなければ Spoonacular で検索する。"""
    if not keyword:
        return []
    return _search_recipes(keyword)


def _search_recipes(keyword: str) -> List[Dict]:
    """Spoonacular: レシピ検索（失敗時は空リストを返す）"""
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": settings.SPOONACULAR_API_KEY,
        "query": keyword,
        "number": 10,
    }

    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code != 200:
            return []

        data = res.json()
        results = data.get("results", []) or []
        return [
            {
                "title": r.get("title"),
                "id": r.get("id"),
                "image": r.get("image"),
            }
            for r in results
        ]
    except requests.RequestException:
        # ネットワーク/タイムアウト等：ページ全体を落とさず空で返す
        return []


def _fetch_recipe_detail(recipe_id: int) -> Optional[Dict]:
    """Spoonacular: レシピ詳細（失敗時はNone）"""
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": settings.SPOONACULAR_API_KEY}

    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            return res.json()
        return None
    except requests.RequestException:
        return None
