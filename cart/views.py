from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from store.models import Product, Order, OrderItem
from .forms import CheckoutForm

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity
        items.append({'product': product, 'quantity': quantity, 'total_price': product.price * quantity})

    return render(request, 'cart/cart_detail.html', {'items': items, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')
    
    total_price = 0
    # Calculate total first (lazy)
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order
            order = Order.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                paid_amount=total_price
            )
            
            # Create Items
            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        vendor=product.vendor,
                        price=product.price,
                        quantity=quantity
                    )
                    # Deduct Stock
                    product.stock -= quantity
                    product.save()
                except Product.DoesNotExist:
                    continue
            
            # Clear Cart
            request.session['cart'] = {}
            return redirect('success')
    else:
        form = CheckoutForm()

    return render(request, 'cart/checkout.html', {'form': form, 'total_price': total_price})

def success(request):
    return render(request, 'cart/success.html')
