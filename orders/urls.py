from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('list/', views.order_list, name='order_list'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:order_id>/', views.order_cancel, name='order_cancel'),
    path('track/', views.order_track, name='order_track'),
    path('track/order/', views.product_track_order, name='product_track_order'),
]