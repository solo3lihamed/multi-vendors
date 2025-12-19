from django.contrib.auth import logout, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Order

def logout_view(request):
    logout(request)
    return redirect('front_page')

@login_required
def my_account(request):
    # Find orders with this user's email (simple linking)
    orders = Order.objects.filter(email=request.user.email).order_by('-created_at')
    return render(request, 'users/my_account.html', {'orders': orders})
