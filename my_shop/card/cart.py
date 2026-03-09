
from decimal import Decimal
from django.conf import settings
from .models import Product, CartItem

#Діма і Данил
class HybridCart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if self.user.is_authenticated:
        # Використовуємо defaults, щоб при створенні встановити 0, 
        # а потім в обох випадках додати потрібну кількість
            item, created = CartItem.objects.get_or_create(
                user=self.user, 
                product=product,
                defaults={'quantity': 0} 
            )
        
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity
            
            item.save()
        else:
            # Логіка для аноніма (тут все було ок, але для чистоти залишаємо)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save_session()

    def minus(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if self.user.is_authenticated:
            item = CartItem.objects.filter(user=self.user, product=product).first()
            if item:
                if update_quantity:
                    item.quantity = max(0, quantity)
                else:
                    item.quantity -= quantity
                
                if item.quantity <= 0:
                    item.delete()
                else:
                    item.save()
        else:
            if product_id in self.cart:
                if update_quantity:
                    self.cart[product_id]['quantity'] = max(0, quantity)
                else:
                    self.cart[product_id]['quantity'] -= quantity

                if self.cart[product_id]['quantity'] <= 0:
                    self.remove_product(product)
                else:
                    self.save_session()
    
    def save_session(self):
        self.session.modified = True

    def remove_product(self, product):
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user, product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save_session()
    
    def clear(self):
        if self.user.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()
        else:
            if settings.CART_SESSION_ID in self.session:
                del self.session[settings.CART_SESSION_ID]
            self.save_session()

    def __iter__(self):
        if self.user.is_authenticated:
            items = CartItem.objects.filter(user=self.user).select_related('product')
            for item in items:
                yield {
                    'product': item.product,
                    'price': item.product.price,
                    'quantity': item.quantity,
                    'total_price': item.get_cost()
                }
        else:
            product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            # Робимо копію даних, щоб не змінювати оригінальний self.cart (Decimal ламає JSON)
            for product in products:
                item_data = self.cart[str(product.id)].copy() 
                price = Decimal(item_data['price'])
                yield {
                    'product': product,
                    'price': price,
                    'quantity': item_data['quantity'],
                    'total_price': price * item_data['quantity']
                }
    
    def __len__(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in CartItem.objects.filter(user=self.user))
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.user.is_authenticated:
            items = CartItem.objects.filter(user=self.user)
            return sum(item.get_cost() for item in items) 
        # Рахуємо суму, перетворюючи рядки в Decimal тільки "на льоту"
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def merge_session_cart_to_db(self, user):
        if not self.cart:
            return
            
        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                db_item, created = CartItem.objects.get_or_create(
                    user=user, product=product,
                    defaults={'quantity': 0}
                )
                db_item.quantity += item_data['quantity']
                db_item.save()
            except Product.DoesNotExist:
                continue
        
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.save_session()