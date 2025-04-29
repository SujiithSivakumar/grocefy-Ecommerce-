from django.db import models
from django.utils.translation import gettext_lazy as _

class Settings(models.Model):
    """
    Site-wide settings configuration model
    """
    SITE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    ]

    # Site Information
    site_title = models.CharField(_('Site Title'), max_length=100, default='GROCEFY')
    site_logo = models.ImageField(_('Site Logo'), upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(_('Favicon'), upload_to='settings/', blank=True, null=True)
    site_description = models.TextField(_('Site Description'), blank=True)
    site_keywords = models.TextField(_('Site Keywords'), blank=True)
    site_status = models.CharField(_('Site Status'), max_length=20, choices=SITE_STATUS_CHOICES, default='active')
    maintenance_message = models.TextField(_('Maintenance Message'), blank=True)
    
    # Contact Information
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    address = models.TextField(_('Address'), blank=True)
    
    # Social Media
    facebook = models.URLField(_('Facebook URL'), blank=True)
    twitter = models.URLField(_('Twitter URL'), blank=True)
    instagram = models.URLField(_('Instagram URL'), blank=True)
    youtube = models.URLField(_('YouTube URL'), blank=True)
    linkedin = models.URLField(_('LinkedIn URL'), blank=True)
    
    # Payment Settings
    currency = models.CharField(_('Currency'), max_length=10, default='USD')
    currency_symbol = models.CharField(_('Currency Symbol'), max_length=5, default='$')
    paypal_client_id = models.CharField(_('PayPal Client ID'), max_length=255, blank=True)
    paypal_secret = models.CharField(_('PayPal Secret'), max_length=255, blank=True)
    paypal_sandbox_mode = models.BooleanField(_('PayPal Sandbox Mode'), default=True)
    
    # Email Settings
    smtp_host = models.CharField(_('SMTP Host'), max_length=100, blank=True)
    smtp_port = models.CharField(_('SMTP Port'), max_length=10, blank=True)
    smtp_username = models.CharField(_('SMTP Username'), max_length=100, blank=True)
    smtp_password = models.CharField(_('SMTP Password'), max_length=100, blank=True)
    smtp_from_email = models.EmailField(_('From Email'), blank=True)
    
    # Footer
    footer_copyright = models.TextField(_('Footer Copyright'), blank=True, default='© 2023 GROCEFY. All rights reserved.')
    
    # Other Settings
    google_analytics = models.CharField(_('Google Analytics ID'), max_length=50, blank=True)
    default_tax_rate = models.DecimalField(_('Default Tax Rate (%)'), max_digits=5, decimal_places=2, default=0)
    
    # Updated timestamp
    updated_at = models.DateTimeField(_('Last Updated'), auto_now=True)
    
    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')
    
    def __str__(self):
        return self.site_title
    
    @classmethod
    def get_settings(cls):
        """
        Get or create settings object
        """
        settings, created = cls.objects.get_or_create(pk=1)
        return settings