from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product, Category, ProductImage
from products.models import Product
from card.models import Order, OrderItem
from django.http import JsonResponse
from card.cart import HybridCart
from users.forms import UserRegistrationForm
import json


#Міша.С
@require_POST
def cart_add(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    

    item_total = 0
    for item in cart:
        if item['product'].id == product.id:
            # Конвертуємо Decimal в float перед відправкою в JsonResponse
            item_total = float(item['total_price'])


    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'item_total_price': item_total,
        'total_price': float(cart.get_total_price()), # float для JSON
    })


#Міша.С
@require_POST
def cart_minus(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.minus(product=product, quantity=1)
    
    item_total = 0
    for item in cart:
        if item['product'].id == product.id:
            item_total = float(item['total_price']) # float для JSON

    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'item_total_price': item_total, 
        'total_price': float(cart.get_total_price()), # ТУТ БУЛА ПОМИЛКА (додано float)
        'message': "Кількість зменшено"
    })


#Міша.С
@require_POST
def cart_add_with_quantity(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)

    try:
        data = json.loads(request.body.decode('utf-8'))
        # Перетворюємо в int і перевіряємо на адекватність
        quantity = int(data.get("quantity", 1))
        
        if quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': "Кількість має бути більшою за 0!"
            }, status=400) # Повертаємо 400 помилку для некоректних даних
            
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)

    # Важливо: перевір, щоб в HybridCart метод add приймав quantity
    cart.add(product=product, quantity=quantity)
    
    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'message': f"Додано {quantity} шт."
    })

# @require_POST
# def card_add_product_detail(request):
#     if request.method == "POST":
#         data_json = json.loads(request.body)
#         product_id = data_json.get("product_id")
#         quantity = data_json.get("quantity")

#         #Зробити валідацію

#         cart = HybridCart(request)
#         try:
#             product = Product.objects.filter(id=product_id, available=True)
#         except Exception as ex:
#             print(ex)
#         cart.add(product=product, quantity=quantity)
#         messages.success(request, "Товар добавлен в корзину!")
#         return redirect('product_detail')
#     else:
#         return HttpResponse(403, "forbidden")

#Міша.С
def cart_remove_product(request, product_id):
    cart = HybridCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart_detail')


#Міша.С
def card_remove(request):
    cart = HybridCart(request)
    cart.clear()
    return redirect('cart_detail')


#Денис
def cart_detail(request):
    cart = HybridCart(request)
    
    cart_product_ids = [item['product'].id for item in cart]
    cart_categories = Product.objects.filter(id__in=cart_product_ids).values_list('category', flat=True)
    
    recommendations = Product.objects.filter(
        category__in=cart_categories,
        available=True
    ).exclude(id__in=cart_product_ids).order_by('?')[:4]
    
    return render(request, 'stors/cart_d.html', {
        'cart': cart,
        'cart_total_items': len(cart),
        'recommendations': recommendations
    })
