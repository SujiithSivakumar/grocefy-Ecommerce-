from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status', 'payment_method', 
                   'transaction_id', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['order__id', 'transaction_id', 'stripe_payment_intent']
    raw_id_fields = ['order']
    readonly_fields = ['created_at', 'updated_at', 'payment_date']
    fieldsets = (
        ('Payment Information', {
            'fields': ('order', 'amount', 'status', 'payment_method')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'stripe_payment_intent')
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
