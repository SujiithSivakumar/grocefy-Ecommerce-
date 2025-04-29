from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem, Coupon
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

def cart_detail(request):
    cart = None
    cart_items = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product)
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart.remove_product(product)
        messages.success(request, f"{product.name} removed from your cart.")
    
    return redirect('cart:cart_detail')

@login_required
def cart_update(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return redirect('cart:cart_detail')
            
        product_ids = request.POST.getlist('qty_id[]')
        quantities = {}
        
        for field_name in request.POST:
            if field_name.startswith('quant['):
                index = field_name.split('[')[1].split(']')[0]
                if index.isdigit():
                    item_index = int(index)
                    if item_index < len(product_ids):
                        product_id = product_ids[item_index]
                        quantity = int(request.POST[field_name])
                        quantities[product_id] = quantity
        
        for product_id, quantity in quantities.items():
            try:
                product = Product.objects.get(id=product_id)
                if quantity > 0:
                    cart.update_quantity(product, quantity)
                else:
                    cart.remove_product(product)
            except Product.DoesNotExist:
                pass
                
        messages.success(request, "Cart updated successfully.")
    
    return redirect('cart:cart_detail')

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        now = timezone.now()
        
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, 
                active=True,
                valid_from__lte=now,
                valid_to__gte=now
            )
            
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart.coupon = coupon
                cart.save()
                messages.success(request, f"Coupon '{code}' applied successfully.")
            else:
                messages.error(request, "You don't have an active cart.")
                
        except Coupon.DoesNotExist:
            messages.error(request, "This coupon does not exist or has expired.")
            
    return redirect('cart:cart_detail')
