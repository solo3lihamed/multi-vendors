from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from .forms import VendorRegistrationForm, VendorStoreForm
from .models import VendorProfile
from store.forms import ProductForm
from store.models import Product

def vendor_register(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            login(request, vendor.user)
            return redirect('vendor_dashboard')
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'vendors/vendor_register.html', {'form': form})

@login_required
def vendor_dashboard(request):
    try:
        vendor = request.user.vendor_profile
    except ObjectDoesNotExist:
        return redirect('create_store')

    products = vendor.products.all()
    # Get all order items belonging to this vendor
    order_items = vendor.order_items.all().order_by('-order__created_at')
    
    # Calculate simple stats
    earnings = sum(item.get_total_price() for item in order_items)
    
    return render(request, 'vendors/dashboard.html', {
        'vendor': vendor, 
        'products': products,
        'order_items': order_items,
        'earnings': earnings
    })

@login_required
def create_store(request):
    # Check if already has profile
    try:
        if request.user.vendor_profile:
            return redirect('vendor_dashboard')
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        form = VendorStoreForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.slug = slugify(vendor.store_name, allow_unicode=True)
            
            # Ensure unique slug
            if VendorProfile.objects.filter(slug=vendor.slug).exists():
                vendor.slug = f"{vendor.slug}-{request.user.id}"
                
            vendor.save()
            
            # Update user role to VENDOR
            request.user.role = 'VENDOR'
            request.user.save()
            
            return redirect('vendor_dashboard')
    else:
        form = VendorStoreForm()
    
    return render(request, 'vendors/create_store.html', {'form': form})

@login_required
def add_product(request):
    vendor = request.user.vendor_profile
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.slug = slugify(product.title, allow_unicode=True) # Simple slugify
            
            # Ensure unique slug
            if Product.objects.filter(slug=product.slug).exists():
                product.slug = f"{product.slug}-{product.id or request.user.id}" # Hacky unique
            
            product.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm()
    return render(request, 'vendors/add_product.html', {'form': form})

def vendors_list(request):
    vendors = VendorProfile.objects.all()
    return render(request, 'vendors/vendors_list.html', {'vendors': vendors})

def vendor_store(request, slug):
    vendor = get_object_or_404(VendorProfile, slug=slug)
    products = vendor.products.filter(is_available=True)
    return render(request, 'vendors/store_detail.html', {'vendor': vendor, 'products': products})

@login_required
def membership(request):
    vendor = request.user.vendor_profile
    if request.method == 'POST':
        # Dummy upgrade
        vendor.is_subscribed = True
        vendor.save()
        return redirect('vendor_dashboard')
    return render(request, 'vendors/membership.html')

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'vendors/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    vendor = request.user.vendor_profile
    product = get_object_or_404(Product, pk=pk, vendor=vendor)
    product.delete()
    return redirect('vendor_dashboard')
