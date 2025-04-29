"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from filebrowser.sites import site as filebrowser_site
from core.views import admin_dashboard
from core.admin import admin_site  # Import the custom admin site

# Custom view to handle admin logout that completely logs out the user
@csrf_protect
def admin_logout_view(request):
    # Check if this is a POST request (Django requires POST for logout)
    if request.method == 'POST':
        auth_logout(request)
        return redirect('core:home')
    # For GET requests, show an error or redirect to a logout confirmation page
    return render(request, 'admin/logout_confirm.html')  # Create this template to confirm logout via POST

urlpatterns = [
    # Our custom admin dashboard takes precedence
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # Regular Django admin URLs
    path('admin/filebrowser/', filebrowser_site.urls),
    path('admin/', admin_site.urls),  # Use the custom admin site instead of admin.site.urls
    
    # Custom admin logout URL that properly logs out from all sessions
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('blog/', include('blog.urls')),  # Include blog app URLs
    path('settings/', include('settings.urls')),  # Include settings app URLs
    path('', include('core.urls')),  # Include core app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
