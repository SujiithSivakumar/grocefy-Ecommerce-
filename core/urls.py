from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('product/quick-view/<int:product_id>/', views.product_quick_view, name='product_quick_view'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/clear-cache/', views.clear_cache, name='clear_cache'),
    path('admin/create-storage-link/', views.create_storage_link, name='create_storage_link'),
    path('admin/change-password/', views.change_password, name='change_password'),
]