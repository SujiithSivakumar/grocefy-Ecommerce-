from .models import Cart

def cart(request):
    """Context processor to make cart data available across all templates."""
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        cart_count = 0
        cart_items = []
    
    return {
        'cart_count': cart_count,
        'cart_items': cart_items
    }