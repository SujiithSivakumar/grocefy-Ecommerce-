from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Banner, Category, Brand, Product, ProductImage, Wishlist, ProductReview

# Import the custom admin site from core.admin
from core.admin import admin_site

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'display_photo', 'status_badge', 'action_buttons')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)
    list_per_page = 10
    
    def display_photo(self, obj):
        if obj.image and hasattr(obj.image, 'url'):  # Make sure image exists and has a URL
            return format_html('<img src="{}" class="img-fluid zoom" style="max-width:80px" />', obj.image.url)
        return format_html('<img src="/static/backend/img/thumbnail-default.jpg" class="img-fluid zoom" style="max-width:80px" />')
    
    def status_badge(self, obj):
        if obj.status == 'active':
            return format_html('<span class="badge badge-success">{}</span>', obj.status)
        return format_html('<span class="badge badge-warning">{}</span>', obj.status)
    
    def action_buttons(self, obj):
        # Use the correct URL pattern names for the custom admin site
        edit_url = reverse('admin:products_banner_change', args=[obj.id])
        delete_url = reverse('admin:products_banner_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    display_photo.short_description = 'Photo'
    status_badge.short_description = 'Status'
    action_buttons.short_description = 'Actions'

    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Comment out custom template until it's created
    # change_list_template = 'admin/products/banner/change_list.html'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at', 'image_preview', 'action_buttons']
    list_filter = ['is_active', 'created_at', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    actions = ['activate_categories', 'deactivate_categories']
    readonly_fields = ['created_at']
    list_per_page = 10
    
    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Use our updated template instead of the simple one
    change_list_template = 'admin/products/category/change_list.html'
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" class="img-fluid zoom" style="max-width:80px" />', obj.image.url)
        return format_html('<img src="/static/backend/img/thumbnail-default.jpg" class="img-fluid zoom" style="max-width:80px" />')
    
    image_preview.short_description = 'Image'
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:products_category_change', args=[obj.id])
        delete_url = reverse('admin:products_category_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    action_buttons.short_description = 'Actions'
    
    def activate_categories(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} categories have been activated.")
    
    activate_categories.short_description = "Activate selected categories"
    
    def deactivate_categories(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} categories have been deactivated.")
    
    deactivate_categories.short_description = "Deactivate selected categories"

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'image_preview', 'action_buttons']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    actions = ['activate_brands', 'deactivate_brands']
    readonly_fields = ['created_at']
    list_per_page = 10
    
    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Use our styled template
    change_list_template = 'admin/products/brand/change_list.html'
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" class="img-fluid zoom" style="max-width:80px" />', obj.image.url)
        return format_html('<img src="/static/backend/img/thumbnail-default.jpg" class="img-fluid zoom" style="max-width:80px" />')
    
    image_preview.short_description = 'Image'
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:products_brand_change', args=[obj.id])
        delete_url = reverse('admin:products_brand_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    action_buttons.short_description = 'Actions'
    
    def activate_brands(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} brands have been activated.")
    
    activate_brands.short_description = "Activate selected brands"
    
    def deactivate_brands(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} brands have been deactivated.")
    
    deactivate_brands.short_description = "Deactivate selected brands"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_feature', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No Image"

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'discount_price', 
                   'discount_percentage', 'stock', 'is_active', 'is_featured', 'image_preview', 'action_buttons']
    list_filter = ['is_active', 'is_featured', 'category', 'brand', 'created_at', 'stock']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'discount_price', 'stock', 'is_active', 'is_featured']
    inlines = [ProductImageInline]
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'discount_percentage']
    list_per_page = 10
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'image_preview')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('stock', 'sku', 'weight', 'dimensions')
        }),
        ('Relations', {
            'fields': ('category', 'brand')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_active', 'mark_as_inactive']
    
    class Media:
        css = {
            'all': ('backend/vendor/datatables/dataTables.bootstrap4.min.css', 'backend/css/custom_admin.css')
        }
        js = (
            'backend/vendor/datatables/jquery.dataTables.min.js',
            'backend/vendor/datatables/dataTables.bootstrap4.min.js',
            'backend/js/custom_admin.js',
        )
    
    # Use our styled template instead of the simplified one
    change_list_template = 'admin/products/product/change_list.html'
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" class="img-fluid zoom" style="max-width:80px" />', obj.image.url)
        return format_html('<img src="/static/backend/img/thumbnail-default.jpg" class="img-fluid zoom" style="max-width:80px" />')
    
    image_preview.short_description = 'Image Preview'
    
    def discount_percentage(self, obj):
        percentage = obj.get_discount_percentage()
        if percentage > 0:
            return format_html('<span style="color: green;">{}</span>%', percentage)
        return "No discount"
    
    discount_percentage.short_description = 'Discount %'
    
    def action_buttons(self, obj):
        edit_url = reverse('admin:products_product_change', args=[obj.id])
        delete_url = reverse('admin:products_product_delete', args=[obj.id])
        return format_html(
            '<div class="action-buttons">'
            '<a href="{}" class="btn btn-primary btn-sm float-left mr-1" style="height:30px; width:30px;border-radius:50%" title="Edit"><i class="fas fa-edit"></i></a> '
            '<a href="{}" class="btn btn-danger btn-sm dltBtn" style="height:30px; width:30px;border-radius:50%" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    
    action_buttons.short_description = 'Actions'
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} products have been marked as featured.")
    
    mark_as_featured.short_description = "Mark selected products as featured"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} products have been marked as not featured.")
    
    mark_as_not_featured.short_description = "Mark selected products as not featured"
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} products have been activated.")
    
    mark_as_active.short_description = "Activate selected products"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} products have been deactivated.")
    
    mark_as_inactive.short_description = "Deactivate selected products"

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at', 'product']
    search_fields = ['user__email', 'product__name']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating_stars', 'status', 'created_at']
    list_filter = ['rating', 'status', 'created_at']
    search_fields = ['user__email', 'product__name', 'review']
    list_editable = ['status']
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #FFD700;">{}</span>', stars)
    
    rating_stars.short_description = 'Rating'
    
    def approve_reviews(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} reviews have been approved.")
    
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} reviews have been disapproved.")
    
    disapprove_reviews.short_description = "Disapprove selected reviews"

# Register all models with the custom admin site
admin_site.register(Banner, BannerAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Brand, BrandAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Wishlist, WishlistAdmin)
admin_site.register(ProductReview, ProductReviewAdmin)
