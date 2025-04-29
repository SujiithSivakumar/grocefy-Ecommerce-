from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse, path
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404

from .models import User
from orders.models import Order

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
        
class OrderInline(admin.TabularInline):
    model = Order
    fields = ('id', 'total_amount', 'status', 'payment_status', 'created_at')
    readonly_fields = ('id', 'total_amount', 'status', 'payment_status', 'created_at')
    extra = 0
    max_num = 5
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_list_template = 'admin/accounts/user/change_list.html'
    
    list_display = ('email', 'username', 'full_name', 'is_active', 'is_staff', 'date_joined', 
                   'last_login', 'orders_count', 'profile_image_preview')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at', 
                     'profile_image_preview', 'orders_count')
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 
                                         'profile_image', 'profile_image_preview')}),
        (_('Address'), {'fields': ('address', 'city', 'country', 'postal_code')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'phone_number', 'profile_image')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
    )
    
    inlines = [OrderInline]
    
    actions = ['activate_users', 'deactivate_users']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.user_list_view), name='accounts_user_changelist'),
        ]
        return custom_urls + urls
    
    def user_list_view(self, request):
        """Custom view to display users list using our template"""
        context = {
            'all_users': self.model.objects.all().prefetch_related('orders').order_by('-date_joined'),
            'cl': self.get_changelist_instance(request),
            'title': 'Users',
            'has_add_permission': self.has_add_permission(request),
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'media': self.media,
        }
        
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.change_list_template, context)
    
    def full_name(self, obj):
        return obj.get_full_name()
    
    full_name.short_description = _('Full Name')
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', 
                             obj.profile_image.url)
        return "No Image"
    
    profile_image_preview.short_description = _('Profile Image')
    
    def orders_count(self, obj):
        count = obj.orders.count()
        url = reverse('admin:orders_order_changelist') + f'?user__id__exact={obj.id}'
        return format_html('<a href="{}">{} orders</a>', url, count)
    
    orders_count.short_description = _('Orders')
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} users have been activated.")
    
    activate_users.short_description = _("Activate selected users")
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} users have been deactivated.")
    
    deactivate_users.short_description = _("Deactivate selected users")
