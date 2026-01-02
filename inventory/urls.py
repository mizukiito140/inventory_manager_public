from django.urls import path
from . import views

app_name = "inventory" 

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('edit/<int:pk>/', views.item_edit, name='item_edit'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
]