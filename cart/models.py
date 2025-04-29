from django.db import models
from django.conf import settings
from products.models import Product
from decimal import Decimal

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def price(self):
        return self.product.discount_price if self.product.discount_price else self.product.price

    @property
    def total_price(self):
        return self.price * self.quantity

class Cart(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('process', 'Progress'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    def add_product(self, product, quantity=1):
        item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

    def remove_product(self, product):
        try:
            item = CartItem.objects.get(cart=self, product=product)
            item.delete()
        except CartItem.DoesNotExist:
            pass

    def update_quantity(self, product, quantity):
        try:
            item = CartItem.objects.get(cart=self, product=product)
            item.quantity = quantity
            item.save()
        except CartItem.DoesNotExist:
            pass

    def clear(self):
        self.items.all().delete()

    @property
    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def get_discount(self):
        if self.coupon:
            return self.coupon.get_discount(self.get_total_price)
        return Decimal('0')

    @property
    def get_total_price_after_discount(self):
        return self.get_total_price - self.get_discount

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(help_text="Percentage value (0 to 100)")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def get_discount(self, amount):
        return Decimal(amount) * (Decimal(self.discount) / Decimal('100'))
