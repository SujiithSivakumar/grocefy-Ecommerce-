from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Settings

def is_admin(user):
    """Check if user is an admin"""
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def settings_view(request):
    """
    View for directly editing settings outside of the admin panel
    This is an alternative to the admin interface
    """
    settings = Settings.get_settings()
    
    if request.method == 'POST':
        # Update site information
        settings.site_title = request.POST.get('site_title', settings.site_title)
        settings.site_description = request.POST.get('site_description', settings.site_description)
        settings.site_keywords = request.POST.get('site_keywords', settings.site_keywords)
        settings.site_status = request.POST.get('site_status', settings.site_status)
        settings.maintenance_message = request.POST.get('maintenance_message', settings.maintenance_message)
        
        # Update contact information
        settings.email = request.POST.get('email', settings.email)
        settings.phone = request.POST.get('phone', settings.phone)
        settings.address = request.POST.get('address', settings.address)
        
        # Update social media
        settings.facebook = request.POST.get('facebook', settings.facebook)
        settings.twitter = request.POST.get('twitter', settings.twitter)
        settings.instagram = request.POST.get('instagram', settings.instagram)
        settings.youtube = request.POST.get('youtube', settings.youtube)
        settings.linkedin = request.POST.get('linkedin', settings.linkedin)
        
        # Update payment settings
        settings.currency = request.POST.get('currency', settings.currency)
        settings.currency_symbol = request.POST.get('currency_symbol', settings.currency_symbol)
        settings.paypal_client_id = request.POST.get('paypal_client_id', settings.paypal_client_id)
        settings.paypal_secret = request.POST.get('paypal_secret', settings.paypal_secret)
        settings.paypal_sandbox_mode = 'paypal_sandbox_mode' in request.POST
        
        # Update footer
        settings.footer_copyright = request.POST.get('footer_copyright', settings.footer_copyright)
        
        # Handle file uploads
        if 'site_logo' in request.FILES:
            settings.site_logo = request.FILES['site_logo']
            
        if 'favicon' in request.FILES:
            settings.favicon = request.FILES['favicon']
        
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings:settings_view')
        
    context = {
        'settings': settings,
    }
    
    return render(request, 'settings/settings_form.html', context)