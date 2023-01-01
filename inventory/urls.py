from django.urls import path
from .views import inventory_list, per_product_view, add_inventory, delete_inventory, update_inventory, handler404


urlpatterns = [
    path("", inventory_list, name="inventory_list"),
    path("inventory/", inventory_list, name="inventory_list"),
    path("per_product_view/<int:pk>", per_product_view, name="per_product_view"),
    path("add_inventory/", add_inventory, name="add_inventory"),
    path("delete_inventory/<int:pk>", delete_inventory, name="delete_inventory"),
    path("update_inventory/<int:pk>", update_inventory, name="update_inventory"),
    path("404.html/", handler404, name="handler404")
]

handler404 = 'inventory.views.handler404'
