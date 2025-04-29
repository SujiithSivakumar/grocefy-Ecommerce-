from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class PostCategory(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    status = models.BooleanField(_('Status'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Post Category')
        verbose_name_plural = _('Post Categories')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class PostTag(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    status = models.BooleanField(_('Status'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Post Tag')
        verbose_name_plural = _('Post Tags')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True, max_length=250)
    summary = models.TextField(_('Summary'))
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to='blog/', blank=True, null=True)
    
    post_cat = models.ForeignKey(PostCategory, on_delete=models.CASCADE, verbose_name=_('Category'))
    tags = models.ManyToManyField(PostTag, blank=True, verbose_name=_('Tags'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    comment = models.TextField(_('Comment'))
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                                     related_name='replies', verbose_name=_('Parent Comment'))
    status = models.BooleanField(_('Status'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Post Comment')
        verbose_name_plural = _('Post Comments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"