from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import InventoryItem
from .forms import InventoryItemForm
from .services.inventory_service import get_items_with_days_left
from .services.spoonacular_service import search_recipes, fetch_recipe_detail


def _handle_item_create(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory:item_list"), None
        return None, form
    return None, InventoryItemForm()


@require_http_methods(["GET", "POST"])
def item_list(request):
    redirect_response, form = _handle_item_create(request)
    if redirect_response:
        return redirect_response

    items = get_items_with_days_left()

    keyword = request.GET.get("q", "").strip()
    recipes = search_recipes(keyword)

    context = {
        "form": form,
        "items": items,
        "recipes": recipes,
        "keyword": keyword,
    }
    return render(request, "inventory/item_list.html", context)


def recipe_detail(request, recipe_id):
    recipe = fetch_recipe_detail(recipe_id)
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