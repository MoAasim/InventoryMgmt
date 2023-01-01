from django.shortcuts import get_object_or_404, redirect, render
from .models import Inventory
from .forms import InventoryForm
from django.contrib import messages

def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, "inventory/inventory_list.html", context=context)


def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "inventory/per_product.html", context=context)


def add_inventory(request):
    if request.method == "POST":
        add_form = InventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            if int(add_form.data['quantity_sold']) > int(add_form.data['quantity_in_stock']):
                messages.warning(request, "quantity sold can not be greater than total quantities")
            new_inventory.sales = float(add_form.data['cost_per_item']) * int(add_form.data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Product successfully added!")
            return redirect("/inventory/")
    else:
        add_form = InventoryForm()
    
    return render(request, "inventory/add_inventory.html", {"form": add_form})


def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.error(request, "Product deleted!")
    return redirect("/inventory/")



def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        update_form = InventoryForm(data=request.POST)
        if update_form.is_valid():
            inventory.name = update_form.data['name']
            inventory.quantity_in_stock = update_form.data['quantity_in_stock']
            inventory.quantity_sold = update_form.data['quantity_sold']
            inventory.cost_per_item = update_form.data['cost_per_item']
            inventory.sales = float(inventory.cost_per_item) * int(inventory.quantity_sold)
            inventory.save()
            messages.success(request, "Product successfully updated!")
            return redirect("/inventory/")
    else:
        init_obj = {
            'name': inventory.name,
            'quantity_in_stock': inventory.quantity_in_stock,
            'quantity_sold': inventory.quantity_sold,
            'cost_per_item': inventory.cost_per_item
        }
        update_form = InventoryForm(data=init_obj)
    
    return render(request, "inventory/update_inventory.html", {"form": update_form})


def handler404(request, exception):
    return render(request, '404.html', status=404)


