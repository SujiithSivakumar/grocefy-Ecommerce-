from .models import Wishlist

def wishlist_count(request):
    """
    Add wishlist count to the context of all templates.
    Returns the number of items in the user's wishlist or 0 if not authenticated.
    """
    count = 0
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    
    return {'wishlist_count': count}