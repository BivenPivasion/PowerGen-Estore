from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from card.models import Order
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from card.cart import HybridCart

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    cart = HybridCart(request)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Ваш профіль оновлено!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # Отримуємо всі замовлення саме цього користувача
    # Використовуємо prefetch_related для оптимізації (щоб не було 100 запитів до БД)
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders,
        'cart_total_items': len(cart)
    }

    return render(request, 'users/profile.html', context)


