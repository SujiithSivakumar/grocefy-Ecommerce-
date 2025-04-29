from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Product

@login_required
def order_create(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items_count = cart_items.count()
        
        if cart_items_count == 0:
            messages.error(request, 'Your cart is empty')
            return redirect('cart:cart_detail')
            
        # Set shipping as free instead of providing choices
        shipping = {'id': 1, 'name': 'Free Shipping', 'price': 0.00}

        if request.method == 'POST':
            order = Order.objects.create(
                user=request.user,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address1=request.POST.get('address1'),
                address2=request.POST.get('address2'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
                postal_code=request.POST.get('postal_code'),
                payment_method=request.POST.get('payment_method'),
                total_amount=cart.get_total_price
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.price,
                    quantity=item.quantity
                )

            # Clear the cart after order is created
            cart_items.delete()
            
            messages.success(request, 'Order placed successfully')
            return redirect('orders:order_detail', order.id)

        context = {
            'cart': cart,
            'cart_items_count': cart_items_count,
            'shipping': shipping
        }
        return render(request, 'orders/order_create.html', context)
        
    except Cart.DoesNotExist:
        messages.error(request, 'You have no active cart')
        return redirect('products:product_list')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully')
    else:
        messages.error(request, 'Order cannot be cancelled')
    return redirect('orders:order_detail', order.id)

def order_track(request):
    """Display the order tracking page."""
    return render(request, 'orders/track.html')

def product_track_order(request):
    """Process the order tracking request."""
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        email = request.POST.get('email')
        
        if not order_number or not email:
            messages.error(request, 'Please provide both order number and email.')
            return redirect('orders:order_track')
            
        try:
            # Try to find the order by order ID and email
            order = Order.objects.get(id=order_number, email=email)
            
            # Create a status message based on the order status
            if order.status == 'pending':
                status_message = 'Your order has been placed and is pending processing.'
            elif order.status == 'processing':
                status_message = 'Your order is currently being processed.'
            elif order.status == 'shipped':
                status_message = 'Your order has been shipped and is on its way.'
            elif order.status == 'delivered':
                status_message = 'Your order has been successfully delivered.'
            elif order.status == 'cancelled':
                status_message = 'Your order was cancelled.'
            else:
                status_message = f'Your order status is: {order.status}'
            
            # Pass the order and status message to the template
            return render(request, 'orders/track_result.html', {
                'order': order,
                'status_message': status_message
            })
            
        except Order.DoesNotExist:
            messages.error(request, 'No order found with the provided order number and email. Please check and try again.')
            return redirect('orders:order_track')
    
    return redirect('orders:order_track')
