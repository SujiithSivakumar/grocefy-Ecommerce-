from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.urls import path, reverse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
from django.core.serializers.json import DjangoJSONEncoder
import json
# Remove the import of User from django.contrib.auth.models
from django.contrib.auth import get_user_model  # Use this instead

# Import UserAdmin but not the User model from Django's auth
from django.contrib.auth.admin import UserAdmin

from orders.models import Order
from products.models import Product, Category, Brand, ProductReview
from accounts.models import User as CustomUser  # Only import the custom User model
from blog.models import Post
from core.models import SiteSetting, Notification, Message  # Removed Banner from imports

# Get the active User model
User = get_user_model()

class CustomAdminSite(admin.AdminSite):
    site_header = 'GROCEFY Admin'
    site_title = 'GROCEFY E-Commerce Admin'
    index_title = 'Dashboard'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(DashboardView.as_view()), name='admin_dashboard'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        # Redirect standard index to custom dashboard
        return self.admin_view(DashboardView.as_view())(request)

# Create custom admin site instance first
admin_site = CustomAdminSite()

# Replace the default admin site
admin.site = admin_site

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'email', 'phone', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_title', 'logo', 'favicon', 'email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url')
        }),
        ('Content', {
            'fields': ('copyright_text', 'about_us', 'privacy_policy', 'terms_conditions')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one site settings instance
        return SiteSetting.objects.count() == 0

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        """Only show notifications for the current user if not superuser"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    
    def has_add_permission(self, request):
        # Disable ability to add messages manually - they should come from contact form
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete messages
        return request.user.is_superuser

# Register models with the custom admin site - Banner is now only registered in products/admin.py
admin_site.register(SiteSetting, SiteSettingAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(Message, MessageAdmin)

# Register the CustomUser model with the custom admin site
admin_site.register(CustomUser, UserAdmin)

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)
        
        # Count boxes data
        context['category_count'] = Category.objects.count()
        context['product_count'] = Product.objects.count()
        context['order_count'] = Order.objects.count()
        context['post_count'] = Post.objects.filter(status='active').count() if hasattr(Post, 'objects') else 0
        
        # Orders statistics
        orders = Order.objects.all()
        recent_orders = orders.order_by('-created_at')[:10]
        context['recent_orders'] = recent_orders
        
        # Generate monthly revenue data for the earnings chart
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
        monthly_revenue = []
        
        # Get current year
        current_year = timezone.now().year
        
        # Generate monthly revenue data
        for month_idx, month_name in enumerate(months, 1):
            month_start = timezone.datetime(current_year, month_idx, 1).date()
            if month_idx < 12:
                month_end = timezone.datetime(current_year, month_idx + 1, 1).date() - timedelta(days=1)
            else:
                month_end = timezone.datetime(current_year, 12, 31).date()
            
            # Only include months up to current date
            if month_end > today:
                continue
                
            month_revenue = orders.filter(created_at__date__gte=month_start, 
                                         created_at__date__lte=month_end).aggregate(
                                         revenue=Sum('total_amount'))['revenue'] or 0
                                         
            monthly_revenue.append({
                'month': month_name,
                'revenue': float(month_revenue)
            })
        
        context['monthly_revenue'] = json.dumps(monthly_revenue, cls=DjangoJSONEncoder)
        
        # Generate user registration data by day of week
        users_by_day = []
        for day in range(1, 8):  # 1=Sunday, 7=Saturday
            # Use the User variable that's defined at the top of the file, which comes from get_user_model()
            count = User.objects.filter(date_joined__week_day=day).count()
            users_by_day.append({
                'day': day,
                'count': count
            })
        
        context['users_by_day'] = json.dumps(users_by_day, cls=DjangoJSONEncoder)
        
        # Ensure we use proper URL naming with namespaces
        context['user_changelist_url'] = reverse('admin:accounts_user_changelist')
        
        return context