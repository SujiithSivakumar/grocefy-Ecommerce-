from django.urls import path
from .views import (
    HomeView, CategoryProductsView, SubCategoryProductsView, 
    ProductDetailView, add_to_wishlist, remove_from_wishlist,
    add_review, search_products, wishlist_view
)

app_name = 'products'

urlpatterns = [
    path('', HomeView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', CategoryProductsView.as_view(), name='category'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', SubCategoryProductsView.as_view(), name='subcategory'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('review/add/<int:product_id>/', add_review, name='add_review'),
    path('search/', search_products, name='search'),
]