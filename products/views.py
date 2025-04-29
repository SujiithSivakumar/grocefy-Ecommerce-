from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Avg
from .models import Product, Category, Banner, ProductReview, Wishlist, Brand
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner.objects.filter(status='active')
        context['categories'] = Category.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(is_featured=True)[:4]
        return context

class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'], is_active=True)
        return Product.objects.filter(category=self.category, is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.filter(parent=None, is_active=True)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(is_featured=True)[:4]
        context['recent_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:5]
        
        # Get max price for price range slider
        max_price = Product.objects.filter(is_active=True).order_by('-price').first()
        if max_price:
            context['max_price'] = max_price.price
            
        return context

class SubCategoryProductsView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.parent_category = get_object_or_404(Category, slug=self.kwargs['category_slug'], is_active=True)
        self.subcategory = get_object_or_404(
            Category, 
            slug=self.kwargs['subcategory_slug'], 
            parent=self.parent_category,
            is_active=True
        )
        return Product.objects.filter(category=self.subcategory, is_active=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.parent_category
        context['subcategory'] = self.subcategory
        context['categories'] = Category.objects.filter(parent=None, is_active=True)
        context['brands'] = Brand.objects.filter(is_active=True)
        context['featured_products'] = Product.objects.filter(is_featured=True)[:4]
        context['recent_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:5]
        
        # Get max price for price range slider
        max_price = Product.objects.filter(is_active=True).order_by('-price').first()
        if max_price:
            context['max_price'] = max_price.price
            
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Get related products from the same category
        related_products = Product.objects.filter(
            category=product.category, 
            is_active=True
        ).exclude(id=product.id)[:4]
        
        # Get product reviews and average rating
        reviews = product.reviews.filter(status=True).order_by('-created_at')
        avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        
        # Check if product is in user's wishlist
        is_in_wishlist = False
        if self.request.user.is_authenticated:
            is_in_wishlist = Wishlist.objects.filter(
                user=self.request.user, 
                product=product
            ).exists()
        
        context.update({
            'related_products': related_products,
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1),
            'review_count': reviews.count(),
            'is_in_wishlist': is_in_wishlist,
            'categories': Category.objects.filter(parent=None, is_active=True),
        })
        return context

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"{product.name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
    
    # Redirect back to the product page
    return redirect('products:product_detail', slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"{product.name} has been removed from your wishlist.")
    else:
        messages.error(request, f"{product.name} is not in your wishlist.")
    
    # Redirect back
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if not rating or not review_text:
            messages.error(request, 'Please provide both rating and review.')
            return redirect('products:product_detail', slug=product.slug)
        
        # Update or create review
        review, created = ProductReview.objects.update_or_create(
            user=request.user, 
            product=product,
            defaults={
                'rating': rating,
                'review': review_text,
                'status': True
            }
        )
        
        if created:
            messages.success(request, 'Thank you! Your review has been submitted.')
        else:
            messages.success(request, 'Your review has been updated.')
            
    return redirect('products:product_detail', slug=product.slug)

def search_products(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(name__icontains=query)
    
    if category_id and category_id != 'all':
        try:
            category = Category.objects.get(id=category_id)
            categories = [category]
            
            # Include subcategories
            if category.children.exists():
                categories.extend(category.children.all())
                
            products = products.filter(category__in=categories)
        except Category.DoesNotExist:
            pass
    
    context = {
        'products': products,
        'query': query,
        'selected_category': category_id,
        'categories': Category.objects.filter(parent=None, is_active=True),
    }
    
    return render(request, 'products/search_results.html', context)

@login_required
def wishlist_view(request):
    """Display all items in the user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'products/wishlist.html', context)
