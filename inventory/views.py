from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Product, Category, StockMovement
from .forms import ProductForm, StockMovementForm
from orders.models import Order

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lt=10).count()
    total_orders = Order.objects.count()
    recent_movements = StockMovement.objects.select_related('product', 'user').order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_orders': total_orders,
        'recent_movements': recent_movements,
    }
    return render(request, 'inventory/dashboard.html', context)

@login_required
def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.select_related('category').all()
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query) |
            Q(color__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'inventory/product_list.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    movements = StockMovement.objects.filter(product=product).order_by('-created_at')
    
    context = {
        'product': product,
        'movements': movements,
    }
    return render(request, 'inventory/product_detail.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli qo‘shildi!')
            return redirect('inventory:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Mahsulot qo‘shish'})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli yangilandi!')
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Mahsulotni tahrirlash'})

@login_required
def stock_movement_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.product = product
            movement.user = request.user
            movement.save()
            
            # Обновляем количество товара
            if movement.movement_type == 'IN':
                product.quantity += movement.quantity
            else:
                product.quantity -= movement.quantity
            product.save()
            
            messages.success(request, 'Mahsulot harakati qayd qilindi!') # Движение товара зафиксировано!
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = StockMovementForm()
    
    context = {
        'form': form,
        'product': product,
        'title': f'Mahsulot harakati: {product.name}'
    }
    return render(request, 'inventory/stock_movement_form.html', context)
