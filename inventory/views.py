from django.shortcuts import get_object_or_404, redirect, render
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm
from django.contrib import messages

#@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, "inventory/inventory_list.html", context=context)


#@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }

    return render(request, "inventory/per_product.html", context=context)


#@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            if int(add_form.data['quantity_sold']) > int(add_form.data['quantity_in_stock']):
                messages.warning(request, "quantity sold can not be greater than total quantities")
            new_inventory.sales = float(add_form.data['cost_per_item']) * int(add_form.data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Product successfully added!")
            return redirect("/inventory/")
    else:
        add_form = AddInventoryForm()
    
    return render(request, "inventory/add_inventory.html", {"form": add_form})


#@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.error(request, "Product deleted!")
    return redirect("/inventory/")



#@login_required
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        update_form = UpdateInventoryForm(data=request.POST)
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
        update_form = UpdateInventoryForm(data=init_obj)
    
    return render(request, "inventory/update_inventory.html", {"form": update_form})


def handler404(request, exception):
    return render(request, '404.html', status=404)

# def handler500(request):
#     return render(request, '500.html', status=500)

