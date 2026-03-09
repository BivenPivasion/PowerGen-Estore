
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Category  
from card.cart import HybridCart 

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(available=True).prefetch_related('images')

    cart = HybridCart(request)
    print(category_slug, "CATEGORY SLUGGGGGGG")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category__in=category.get_descendants(include_self=True))

    query = request.GET.get('search')
    if query:
        products = products.filter(name__icontains=query).select_related("category")
    featured_products = Product.objects.filter(available=True, is_featured=True)[:4]

    print(products)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'cart_total_items': len(cart),
        'featured_products': featured_products,
    }
    return render(request, 'stors/prodli.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    specifications = product.specifications.select_related('feature').all()
    gallery = product.images.all()
    cart = HybridCart(request)

    return render(request, 'stors/products_detail.html', {
        'product': product,
        'specifications': specifications,
        'cart_total_items': len(cart),
        'gallery': gallery,
    })

# сделать добавление в корзину