from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, Customer, OrderItem
from .forms import OrderForm, CustomerForm
from inventory.models import Product


@login_required
def order_list(request):
    orders = Order.objects.select_related('customer').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Buyurtma muvaffaqiyatli yaratildi!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Buyurtma yaratish'})


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'orders/customer_list.html', {'customers': customers})


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ta`minotchi muvaffaqiyatli qo‘shildi !')
            return redirect('orders:customer_list')
    else:
        form = CustomerForm()

    return render(request, 'orders/customer_form.html', {'form': form, 'title': 'Ta`minotchi kiritish'})


@login_required
def delivery_list(request):
    orders = Order.objects.select_related('customer').order_by('-created_at')
    return render(request, 'orders/delivery_list.html', {'orders': orders})

@login_required
def delivery_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yetkazib berish ma`lumotlari yangilandi!')
            return redirect('orders:delivery_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Yetkazib berishni yangilash'})