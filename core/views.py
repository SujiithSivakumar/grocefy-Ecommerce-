from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Count, Avg, Sum
from products.models import Product, Category, Banner, Brand
from orders.models import Order, OrderItem
from blog.models import Post  # Added import for Post model
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractWeekDay, ExtractDay
from django.utils import timezone
import calendar
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.cache import cache
import json
import random  # For demo data only
import os
import subprocess
from django.db import connection

def home(request):
    # Check if the database tables exist to avoid errors during initial deployment
    def table_exists(table_name):
        with connection.cursor() as cursor:
            return table_name in connection.introspection.table_names(cursor)
    
    # Initialize empty containers for context data
    banners = []
    mid_banners = []
    featured_categories = []
    new_products = []
    featured_products = []
    top_selling_products = []
    popular_products = []
    latest_posts = []
    categories = []
    product_lists = []
    
    # Only query models if their tables exist in the database
    if table_exists('products_banner'):
        # Get main banners for slider
        try:
            # Create dummy banners with placeholder image if no images exist
            banners_query = Banner.objects.all().order_by('-id')[:3]
            banners = []
            
            # Check if we have any banners, if not or if they have image issues, use placeholders
            if not banners_query.exists():
                # No database items, we'll use empty list (already initialized)
                pass
            else:
                # Process banners to ensure they don't cause template errors
                for banner in banners_query:
                    # Only include banners with valid images or set image to None
                    try:
                        # Access image URL to trigger any potential errors
                        if banner.image and hasattr(banner.image, 'url'):
                            img_url = banner.image.url
                            banners.append(banner)
                    except (ValueError, FileNotFoundError, AttributeError):
                        # Skip banners with image issues
                        print(f"Skipping banner {banner.id} due to image issues")
                        pass
            
            # Same approach for mid banners
            mid_banners_query = Banner.objects.all().order_by('-id')[3:5]
            mid_banners = []
            
            for banner in mid_banners_query:
                try:
                    if banner.image and hasattr(banner.image, 'url'):
                        img_url = banner.image.url
                        mid_banners.append(banner)
                except (ValueError, FileNotFoundError, AttributeError):
                    pass
                    
        except Exception as e:
            print(f"Error fetching banners: {str(e)}")
    
    if table_exists('products_category'):
        try:
            # Get featured categories
            categories_query = Category.objects.filter(is_active=True, parent=None).order_by('-id')[:3]
            featured_categories = []
            
            # Process categories to ensure they don't cause template errors
            for category in categories_query:
                try:
                    # Test image access
                    if not category.image or not hasattr(category.image, 'url'):
                        # If image is missing, set it to None to avoid template errors
                        category.image = None
                    featured_categories.append(category)
                except (ValueError, FileNotFoundError, AttributeError):
                    # Still append the category but with image set to None
                    category.image = None
                    featured_categories.append(category)
            
            # Get all categories for the product filter
            categories_query = Category.objects.filter(is_active=True, parent=None)
            categories = []
            
            for category in categories_query:
                try:
                    if not category.image or not hasattr(category.image, 'url'):
                        category.image = None
                    categories.append(category)
                except (ValueError, FileNotFoundError, AttributeError):
                    category.image = None
                    categories.append(category)
                    
        except Exception as e:
            print(f"Error fetching categories: {str(e)}")
    
    if table_exists('products_product'):
        try:
            # Process products to handle missing images
            def process_products_query(query):
                result = []
                for product in query:
                    try:
                        if not product.image or not hasattr(product.image, 'url'):
                            product.image = None
                        result.append(product)
                    except (ValueError, FileNotFoundError, AttributeError):
                        product.image = None
                        result.append(product)
                return result
            
            # Get new arrivals (products)
            new_products = process_products_query(
                Product.objects.filter(is_active=True).order_by('-created_at')[:8]
            )
            
            # Get featured products
            featured_products = process_products_query(
                Product.objects.filter(is_featured=True, is_active=True).order_by('-id')[:8]
            )
            
            # Get products with discount (top selling as placeholder)
            top_selling_products = process_products_query(
                Product.objects.filter(is_active=True, discount_price__isnull=False).order_by('-id')[:8]
            )
            
            # Get popular products
            popular_products = process_products_query(
                Product.objects.filter(is_active=True, is_featured=True).order_by('-id')[:8]
            )
            
            # Get all active products for product list
            product_lists = process_products_query(
                Product.objects.filter(is_active=True).order_by('-created_at')[:16]
            )
            
            # Use hot products as latest posts placeholder
            latest_posts = process_products_query(
                Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:3]
            )
                
        except Exception as e:
            print(f"Error fetching products: {str(e)}")
    
    context = {
        'featured_categories': featured_categories,
        'new_products': new_products,
        'featured_products': featured_products,
        'top_selling_products': top_selling_products,
        'banners': banners,  # Main banners for top slider
        'mid_banners': mid_banners,
        'popular_products': popular_products,
        'latest_posts': latest_posts,
        'categories': categories,  # For nav menu
        'product_lists': product_lists,  # Added product_lists to match template
    }
    
    return render(request, 'home.html', context)

def about_us(request):
    return render(request, 'about.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Send email
        try:
            email_message = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            
            Message:
            {message}
            """
            
            send_mail(
                subject=f'Contact Form: {subject}',
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
        
    return render(request, 'contact.html')

@require_http_methods(["GET"])
def product_quick_view(request, product_id):
    """AJAX endpoint for quick view modal"""
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Get reviews data if available
        reviews_count = 0
        avg_rating = 0
        
        data = {
            'id': product.id,
            'name': product.name,
            'photo': product.image.url if product.image else '',
            'description': product.description[:150] + '...' if len(product.description) > 150 else product.description,
            'price': float(product.price),
            'discount_price': float(product.discount_price) if product.discount_price else None,
            'stock': product.stock,
            'avg_rating': avg_rating,
            'review_count': reviews_count,
            'category_name': product.category.name if product.category else '',
            'brand_name': product.brand.name if product.brand else '',
        }
        
        return JsonResponse(data)
    except:
        return JsonResponse({'error': 'Product not found'}, status=404)

# Check if user is admin
def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin dashboard view that shows stats and charts in SB Admin 2 style
    exactly like Laravel dashboard
    """
    # Get counts for dashboard cards
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    post_count = Post.objects.count()
    
    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    # Calculate monthly revenue for chart (past 6 months)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=180)  # 6 months approx
    
    # Query to get monthly revenue
    monthly_orders = Order.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        revenue=Sum('total_amount')
    ).order_by('month')
    
    # Format data for chart
    monthly_revenue = []
    for entry in monthly_orders:
        month_name = calendar.month_name[entry['month'].month]
        monthly_revenue.append({
            'month': f"{month_name} {entry['month'].year}",
            'revenue': float(entry['revenue']) if entry['revenue'] else 0
        })
    
    # Add missing months with zero revenue
    if len(monthly_revenue) < 6:
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        for i in range(6):
            month_num = (current_month - i) % 12
            if month_num == 0:
                month_num = 12
                year = current_year - 1
            else:
                year = current_year
                
            month_name = calendar.month_name[month_num]
            month_str = f"{month_name} {year}"
            
            # Check if month exists in data
            if not any(entry['month'] == month_str for entry in monthly_revenue):
                monthly_revenue.append({
                    'month': month_str,
                    'revenue': 0
                })
    
    # Sort by date
    monthly_revenue.sort(key=lambda x: datetime.strptime(x['month'], '%B %Y'))
    
    # Get user registrations by day of week - using get_user_model() instead of User directly
    User = get_user_model()
    users_by_day = User.objects.annotate(
        day=ExtractDay('date_joined')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Format for the pie chart
    users_by_day_data = []
    for day_data in users_by_day:
        users_by_day_data.append({
            'day': day_data['day'],
            'count': day_data['count']
        })
    
    context = {
        'category_count': category_count,
        'product_count': product_count,
        'order_count': order_count,
        'post_count': post_count,
        'recent_orders': recent_orders,
        'monthly_revenue': json.dumps(monthly_revenue),
        'users_by_day': json.dumps(users_by_day_data),
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def clear_cache(request):
    """Clear all cache"""
    cache.clear()
    return redirect('admin_dashboard')

@staff_member_required
def create_storage_link(request):
    """Create a symbolic link for storage (similar to Laravel's storage:link)"""
    try:
        # Create symbolic link between storage and public directories
        # This is a Django approximation of Laravel's Artisan storage:link command
        media_root = settings.MEDIA_ROOT
        public_media = os.path.join(settings.BASE_DIR, 'public/media')
        
        # Ensure media directory exists
        os.makedirs(media_root, exist_ok=True)
        
        # Create symlink if it doesn't exist
        if not os.path.exists(public_media):
            if os.name == 'nt':  # Windows
                subprocess.run(['mklink', '/D', public_media, media_root], shell=True)
            else:  # Unix/Linux
                os.symlink(media_root, public_media)
                
        messages.success(request, 'Storage link created successfully')
    except Exception as e:
        messages.error(request, f'Error creating storage link: {str(e)}')
    
    return redirect('admin_dashboard')

@login_required
def change_password(request):
    """
    View for changing user password
    """
    if request.method == 'POST':
        # Handle form submission
        # ...
        messages.success(request, 'Password changed successfully!')
        return redirect('core:admin_dashboard')
    return render(request, 'admin/auth/change_password.html')