from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()

class Banner(models.Model):
    """Banner model for storing website banner information"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/banners/', 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    status = models.CharField(max_length=10, choices=(
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ), default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['-created_at']

class SiteSetting(models.Model):
    """Model for storing site-wide settings"""
    site_title = models.CharField(max_length=100, default="GROCEFY")
    logo = models.ImageField(upload_to='photos/site/', blank=True, null=True,
                           validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    favicon = models.ImageField(upload_to='photos/site/', blank=True, null=True,
                              validators=[FileExtensionValidator(['ico', 'png'])])
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    copyright_text = models.CharField(max_length=255, blank=True, null=True)
    about_us = RichTextField(blank=True, null=True)
    privacy_policy = RichTextField(blank=True, null=True)
    terms_conditions = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.site_title
    
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Message(models.Model):
    """Model for storing contact messages from users"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.subject} - {self.name}"