from django.contrib import admin
from django.utils.html import format_html
from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    """
    Custom admin for site settings with fieldsets for better organization
    """
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'site_logo', 'favicon', 'site_description', 
                      'site_keywords', 'site_status', 'maintenance_message'),
            'classes': ('wide',),
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address'),
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'youtube', 'linkedin'),
            'classes': ('collapse',),
        }),
        ('Payment Settings', {
            'fields': ('currency', 'currency_symbol', 'paypal_client_id', 
                      'paypal_secret', 'paypal_sandbox_mode'),
        }),
        ('Email Settings', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 
                      'smtp_password', 'smtp_from_email'),
            'classes': ('collapse',),
        }),
        ('Footer', {
            'fields': ('footer_copyright',),
        }),
        ('Other Settings', {
            'fields': ('google_analytics', 'default_tax_rate'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('updated_at', 'logo_preview', 'favicon_preview')
    list_display = ('site_title', 'logo_preview', 'email', 'site_status', 'updated_at')
    
    def logo_preview(self, obj):
        if obj.site_logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 200px;" />', obj.site_logo.url)
        return "No Logo"
    
    logo_preview.short_description = 'Logo Preview'
    
    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="max-height: 32px; max-width: 32px;" />', obj.favicon.url)
        return "No Favicon"
    
    favicon_preview.short_description = 'Favicon Preview'
    
    def has_add_permission(self, request):
        # Prevent creating more than one Settings instance
        return Settings.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the Settings instance
        return False