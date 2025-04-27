from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# This view displays all the products
def product_list(request):
    products = Product.objects.all()  # Retrieve all products from the database
    return render(request, 'store/product_list.html', {'products': products})  # Pass products to the template

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to the product list page
    else:
        form = ProductForm()

    # Debugging the context being passed to the template
    print(f"Form: {form}")
    print(f"Is form valid: {form.is_valid() if request.method == 'POST' else 'N/A'}")
    
    return render(request, 'store/add_product.html', {'form': form})
