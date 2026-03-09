from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
from card.models import Order

User = get_user_model()


class Payment(models.Model):
    STATUS_CHOICES = (
        ('init', 'Init'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('sandbox', 'Sandbox'),
        ('reversed', 'Reversed'),
        ('expired', 'Expired'),
        ('error', 'Error'),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    liqpay_order_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='init'
    )

    liqpay_data = models.TextField()
    liqpay_signature = models.TextField()

    liqpay_response = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.liqpay_order_id}"
