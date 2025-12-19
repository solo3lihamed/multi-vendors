from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    return render(request, 'store/product_detail.html', {'product': product})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_available=True)
    return render(request, 'store/category_detail.html', {'category': category, 'products': products})

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(is_available=True)
    
    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'store/search.html', {'products': products, 'query': query})
