from django.shortcuts import render, redirect, get_object_or_404
from card.models import Order, OrderItem
from card.cart import HybridCart
from django.http import JsonResponse

def checkout(request):
    cart = HybridCart(request)
    if len(cart) == 0:
        return redirect('product_list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name') or (request.user.get_full_name() if request.user.is_authenticated else '')
        email = request.POST.get('email') or (request.user.email if request.user.is_authenticated else '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        postal_code = request.POST.get('postal_code', '')
        delivery_method = request.POST.get('delivery_method', 'courier')
        payment_method = request.POST.get('payment_method', 'cod')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            delivery_method=delivery_method,
            payment_method=payment_method
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        if payment_method == 'online':
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'order_id': order.id
                })
        else:
            return redirect('order_success', order_id=order.id)

    initial = {}
    if request.user.is_authenticated:
        print(request.user)
        full_name = f"{request.user.first_name} {request.user.last_name}"
        print(full_name)
        initial['full_name'] = full_name
        initial['email'] = request.user.email
        # if hasattr(request.user, 'profile') and request.user.profile.phone:
        #     initial['phone'] = request.user.profile.number

    return render(request, 'stors/checkout.html', {'cart': cart, 'cart_total_items': len(cart), 'initial': initial})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'stors/order_success.html', {'order': order})