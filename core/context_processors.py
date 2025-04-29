from products.models import Product, Category, Brand
from blog.models import Post, PostCategory
from orders.models import Order
from django.contrib.auth import get_user_model

def categories_processor(request):
    """Context processor to add categories to context."""
    categories = Category.objects.filter(is_active=True).order_by('name')
    return {'global_categories': categories}

def admin_stats(request):
    """Context processor to provide admin dashboard statistics."""
    # Only compute these stats for admin pages to avoid unnecessary DB queries
    if not request.path.startswith('/admin/'):
        return {}
        
    User = get_user_model()
    
    try:
        stats = {
            'total_products': Product.objects.filter(is_active=True).count(),
            'total_categories': Category.objects.filter(is_active=True).count(),
            'total_orders': Order.objects.count(),
            'total_users': User.objects.count(),
            'total_posts': Post.objects.count(),
            'total_brands': Brand.objects.count(),
        }
    except:
        # If any of the models don't exist yet (migrations not applied), provide defaults
        stats = {
            'total_products': 0,
            'total_categories': 0,
            'total_orders': 0,
            'total_users': 0,
            'total_posts': 0,
            'total_brands': 0,
        }
        
    return {'admin_stats': stats}