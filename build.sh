#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Set up media directory structure
mkdir -p media/banners
mkdir -p media/categories
mkdir -p media/brands
mkdir -p media/products
mkdir -p media/images
mkdir -p staticfiles/images

# Run migrations
python manage.py migrate

# Create initial data through a Python script
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from products.models import Category, Brand, Banner, Product
import os
from django.conf import settings
import shutil

User = get_user_model()

# Create a superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'render2025')
    print("Superuser created successfully!")

# Create sample categories if none exist
if Category.objects.count() == 0:
    category1 = Category.objects.create(name="Fruits & Vegetables", slug="fruits-vegetables", is_active=True)
    category2 = Category.objects.create(name="Dairy & Bakery", slug="dairy-bakery", is_active=True)
    category3 = Category.objects.create(name="Staples", slug="staples", is_active=True)
    print(f"Created {Category.objects.count()} sample categories")

# Create sample brands if none exist
if Brand.objects.count() == 0:
    brand1 = Brand.objects.create(name="Fresh Farms", slug="fresh-farms", is_active=True)
    brand2 = Brand.objects.create(name="Nature's Best", slug="natures-best", is_active=True)
    brand3 = Brand.objects.create(name="Healthy Choice", slug="healthy-choice", is_active=True)
    print(f"Created {Brand.objects.count()} sample brands")

# Create sample banner if none exist
if Banner.objects.count() == 0:
    banner = Banner.objects.create(
        title="Welcome to Grocefy",
        slug="welcome-banner",
        description="Your one-stop shop for fresh groceries",
        status="active"
    )
    print(f"Created {Banner.objects.count()} sample banner")

# Create sample products if none exist
if Product.objects.count() == 0 and Category.objects.count() > 0 and Brand.objects.count() > 0:
    category = Category.objects.first()
    brand = Brand.objects.first()
    
    product1 = Product.objects.create(
        name="Fresh Apples",
        slug="fresh-apples",
        category=category,
        brand=brand,
        description="Crisp and juicy apples fresh from the orchard",
        price=2.99,
        stock=100,
        is_active=True,
        is_featured=True
    )
    
    product2 = Product.objects.create(
        name="Organic Bananas",
        slug="organic-bananas",
        category=category,
        brand=brand,
        description="Sweet and nutritious organic bananas",
        price=1.99,
        discount_price=1.49,
        stock=150,
        is_active=True,
        is_featured=True
    )
    
    product3 = Product.objects.create(
        name="Fresh Milk",
        slug="fresh-milk",
        category=Category.objects.get(name="Dairy & Bakery"),
        brand=Brand.objects.get(name="Nature's Best"),
        description="Farm fresh milk",
        price=3.49,
        stock=50,
        is_active=True,
        is_featured=False
    )
    
    print(f"Created {Product.objects.count()} sample products")

# Create a default logo in static folder
static_images_dir = os.path.join(settings.STATIC_ROOT, 'images')
os.makedirs(static_images_dir, exist_ok=True)

# Create a simple text file explaining about media files
with open(os.path.join(settings.MEDIA_ROOT, 'README.txt'), 'w') as f:
    f.write("""
    This directory is for uploaded media files.
    
    In the deployed environment, image files uploaded through the admin interface
    will be stored here but will be lost on redeployment due to Render's ephemeral filesystem.
    
    For a production environment, consider using an external storage service like AWS S3 
    or Cloudinary for persistent media storage.
    """)

print("Media directories created successfully.")
EOF

# Collect static files
python manage.py collectstatic --no-input