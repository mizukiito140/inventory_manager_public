from django.urls import path
from .views import item_list

app_name = "inventory"

urlpatterns = [
    path("", item_list, name="item_list"),
]