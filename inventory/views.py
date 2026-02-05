from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET
from django.http import Http404

from .models import InventoryItem
from .forms import InventoryItemForm
from .services.inventory_service import get_items
from .services.spoonacular_service import search_recipes, fetch_recipe_detail

@require_http_methods(["GET", "POST"])
def item_list(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list")
    else:
        form = InventoryItemForm()

    items = get_items()
    keyword = request.GET.get("q", "").strip()
    recipes = search_recipes(keyword)

    return render(request, "inventory/item_list.html", {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    })


@require_GET
def recipe_search(request):
    """
    /items/recipe-search/ 用
    レシピ検索結果のHTML“だけ”を返す（部分テンプレ）。
    item_list.html 側で fetch して右カラムだけ差し替える想定。
    """
    keyword = request.GET.get("q", "").strip()
    recipes = search_recipes(keyword)

    return render(
        request,
        "inventory/_recipe_results.html",
        {
            "recipes": recipes,
            "keyword": keyword,
        },
    )


def recipe_detail(request, recipe_id):
    recipe = fetch_recipe_detail(recipe_id)
    if recipe is None:
        raise Http404("Recipe not found")
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
