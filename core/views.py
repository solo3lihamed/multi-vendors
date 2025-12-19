from django.shortcuts import render
from store.models import Product

def front_page(request):
    products = Product.objects.filter(is_available=True)[0:6]
    return render(request, 'core/front_page.html', {'products': products})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
