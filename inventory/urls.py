from django.urls import path
from .views import item_list, item_edit, item_delete, recipe_detail, recipe_search

app_name = "inventory"

urlpatterns = [
    # 在庫一覧 & アイテム登録
    path("", item_list, name="item_list"),
    
    path("recipe-search/", recipe_search, name="recipe_search"),
    # アイテム編集・削除
    path("edit/<int:pk>/", item_edit, name="item_edit"),
    path("delete/<int:pk>/", item_delete, name="item_delete"),

    # レシピ詳細
    path("recipe/<int:recipe_id>/", recipe_detail, name="recipe_detail"),
]
