from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
import csv
import datetime
from .models import Order, OrderItem, Coupon, Shipping

# Import the custom admin site
from core.admin import admin_site

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_info', 'price', 'total_price']
    fields = ['product', 'product_info', 'quantity', 'price', 'total_price']
    
    def product_info(self, obj):
        if (obj.product):
            url = reverse('admin:products_product_change', args=[obj.product.id])
            if obj.product.image:
                return format_html('<a href="{}" target="_blank"><img src="{}" style="height: 30px;" /> {}</a>', 
                           url, obj.product.image.url, obj.product.name)
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.product.name)
        return "Product not available"
    
    product_info.short_description = 'Product Info'
    
    def total_price(self, obj):
        return format_html('${:.2f}', obj.get_total_price())
    
    total_price.short_description = 'Total'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_info', 'total_amount', 'final_amount', 'status_colored', 
                   'payment_status_colored', 'payment_method', 'created_at', 'action_buttons']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'phone']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'final_amount', 'order_items_count']
    list_per_page = 10
    fieldsets = (
        ('Customer Information', {
            'fields': (('first_name', 'last_name'), 'email', 'phone', 'user')
        }),
        ('Shipping Information', {
            'fields': ('address', ('city', 'country', 'postal_code'))
        }),
        ('Order Details', {
            'fields': (('total_amount', 'shipping_cost', 'discount_amount', 'final_amount'),
                      ('shipping', 'coupon'),
                      ('status', 'payment_status', 'payment_method'),
                      'payment_id', 'notes', 'order_items_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['export_to_csv', 'mark_as_processing', 'mark_as_shipped', 
               'mark_as_delivered', 'mark_as_cancelled', 'mark_payment_as_completed']
    
    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Use our properly styled template instead of the simple template
    change_list_template = 'admin/orders/order/change_list.html'
    
    def customer_info(self, obj):
        return format_html('{} {}<br/><small>{}</small>', 
                          obj.first_name, obj.last_name, obj.email)
    
    customer_info.short_description = 'Customer'
    
    def status_colored(self, obj):
        colors = {
            'pending': 'blue',
            'processing': 'orange',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
        }
        return format_html('<span style="color: {};">{}</span>', 
                          colors.get(obj.status, 'black'), obj.get_status_display())
    
    status_colored.short_description = 'Status'
    
    def payment_status_colored(self, obj):
        colors = {
            'pending': 'blue',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'purple',
        }
        return format_html('<span style="color: {};">{}</span>', 
                          colors.get(obj.payment_status, 'black'), obj.get_payment_status_display())
    
    payment_status_colored.short_description = 'Payment'
    
    def final_amount(self, obj):
        return format_html('${:.2f}', obj.get_final_amount())
    
    final_amount.short_description = 'Final Amount'
    
    def order_items_count(self, obj):
        return obj.get_total_items()
    
    order_items_count.short_description = 'Number of Items'
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:orders_order_change', args=[obj.id])
        delete_url = reverse('admin:orders_order_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    action_buttons.short_description = 'Actions'
    
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders-{}.csv'.format(
            datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Customer', 'Email', 'Phone', 'Total Amount', 
                        'Status', 'Payment Status', 'Created At'])
        
        for order in queryset:
            writer.writerow([
                order.id,
                f"{order.first_name} {order.last_name}",
                order.email,
                order.phone,
                order.get_final_amount(),
                order.get_status_display(),
                order.get_payment_status_display(),
                order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    export_to_csv.short_description = 'Export selected orders to CSV'
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f"{queryset.count()} orders have been marked as processing.")
    
    mark_as_processing.short_description = "Mark selected orders as processing"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f"{queryset.count()} orders have been marked as shipped.")
    
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f"{queryset.count()} orders have been marked as delivered.")
    
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} orders have been marked as cancelled.")
    
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"
    
    def mark_payment_as_completed(self, request, queryset):
        queryset.update(payment_status='completed')
        self.message_user(request, f"Payment status for {queryset.count()} orders have been marked as completed.")
    
    mark_payment_as_completed.short_description = "Mark payment as completed"

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'type', 'value_display', 'min_order_value', 
                   'max_uses', 'used_count', 'validity_status', 'status', 'date_range']
    list_filter = ['type', 'status', 'start_date', 'end_date']
    search_fields = ['code']
    list_editable = ['status']
    readonly_fields = ['used_count']
    actions = ['activate_coupons', 'deactivate_coupons']
    
    def value_display(self, obj):
        if obj.type == 'fixed':
            return format_html('${:.2f}', obj.value)
        return f"{obj.value}%"
    
    value_display.short_description = 'Value'
    
    def validity_status(self, obj):
        now = datetime.datetime.now(datetime.timezone.utc)
        if not obj.status:
            return format_html('<span style="color: red;">Inactive</span>')
        if now < obj.start_date:
            return format_html('<span style="color: blue;">Not Started</span>')
        if now > obj.end_date:
            return format_html('<span style="color: red;">Expired</span>')
        if obj.used_count >= obj.max_uses:
            return format_html('<span style="color: red;">Maxed Out</span>')
        return format_html('<span style="color: green;">Active</span>')
    
    validity_status.short_description = 'Validity'
    
    def date_range(self, obj):
        return format_html('{} to {}', 
                          obj.start_date.strftime('%Y-%m-%d'), 
                          obj.end_date.strftime('%Y-%m-%d'))
    
    date_range.short_description = 'Date Range'
    
    def activate_coupons(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} coupons have been activated.")
    
    activate_coupons.short_description = "Activate selected coupons"
    
    def deactivate_coupons(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} coupons have been deactivated.")
    
    deactivate_coupons.short_description = "Deactivate selected coupons"

class ShippingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'status', 'created_at', 'updated_at', 'action_buttons']
    list_filter = ['status', 'created_at']
    search_fields = ['title']
    list_editable = ['price', 'status']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 10
    date_hierarchy = 'created_at'
    actions = ['activate_shipping', 'deactivate_shipping']
    
    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Use our properly styled template instead of the simple one
    change_list_template = 'admin/orders/shipping/change_list.html'
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:orders_shipping_change', args=[obj.id])
        delete_url = reverse('admin:orders_shipping_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    action_buttons.short_description = 'Actions'
    
    def activate_shipping(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} shipping methods have been activated.")
    
    activate_shipping.short_description = "Activate selected shipping methods"
    
    def deactivate_shipping(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} shipping methods have been deactivated.")
    
    deactivate_shipping.short_description = "Deactivate selected shipping methods"

# Register models with the custom admin site
admin_site.register(Order, OrderAdmin)
admin_site.register(Coupon, CouponAdmin)
admin_site.register(Shipping, ShippingAdmin)
