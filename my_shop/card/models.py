from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

#Діма, Данил
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.product.price * self.quantity

#Руслан
class Order(models.Model):
    PAYMENT_METHODS = [
        ('online', 'Онлайн оплата'),
        ('cod', 'Оплата при получении'),
    ]

    DELIVERY_METHODS = [
        ('courier', 'Курьером'),
        ('branch', 'На отделение'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='card_orders',
        null=True,
        blank=True
    ) #In prod remove nullabele and blank
    full_name = models.CharField("ФИО", max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cod')
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS, default='courier')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField("Оплачено", default=False)



    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def str(self):
        return f"Заказ {self.id}"

    @property
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


#Діма, Данил
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity