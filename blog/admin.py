from django.contrib import admin
from django.utils.html import format_html
from .models import Post, PostCategory, PostTag, PostComment

# Import the custom admin site
from core.admin import admin_site

class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 0
    fields = ['user', 'comment', 'status', 'created_at']
    readonly_fields = ['created_at']

# Use ModelAdmin without the decorator
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['title']
    list_editable = ['status']
    actions = ['enable_status', 'disable_status']
    
    def enable_status(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} categories have been enabled.")
    
    enable_status.short_description = "Enable selected categories"
    
    def disable_status(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} categories have been disabled.")
    
    disable_status.short_description = "Disable selected categories"

class PostTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['title']
    list_editable = ['status']
    actions = ['enable_status', 'disable_status']
    
    def enable_status(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} tags have been enabled.")
    
    enable_status.short_description = "Enable selected tags"
    
    def disable_status(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} tags have been disabled.")
    
    disable_status.short_description = "Disable selected tags"

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'post_cat', 'author', 'status', 'created_at']
    list_filter = ['post_cat', 'status', 'created_at']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PostCommentInline]
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'summary', 'description', 'quote')
        }),
        ('Media', {
            'fields': ('photo', 'image_preview')
        }),
        ('Relations', {
            'fields': ('post_cat', 'tags')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['make_active', 'make_inactive']
    
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.photo.url)
        return "No Image"
    
    image_preview.short_description = 'Image Preview'
    
    def status_colored(self, obj):
        if obj.status == 'active':
            return format_html('<span style="color: green;">Active</span>')
        return format_html('<span style="color: red;">Inactive</span>')
    
    status_colored.short_description = 'Status'
    
    def comment_count(self, obj):
        return obj.postcomment_set.count()
    
    comment_count.short_description = 'Comments'
    
    def make_active(self, request, queryset):
        queryset.update(status='active')
        self.message_user(request, f"{queryset.count()} posts have been activated.")
    
    make_active.short_description = "Mark selected posts as active"
    
    def make_inactive(self, request, queryset):
        queryset.update(status='inactive')
        self.message_user(request, f"{queryset.count()} posts have been deactivated.")
    
    make_inactive.short_description = "Mark selected posts as inactive"

class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['comment', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    actions = ['approve_comments', 'reject_comments']
    
    def comment_excerpt(self, obj):
        if len(obj.comment) > 50:
            return obj.comment[:50] + "..."
        return obj.comment
    
    comment_excerpt.short_description = 'Comment'
    
    def approve_comments(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, f"{queryset.count()} comments have been approved.")
    
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, f"{queryset.count()} comments have been rejected.")
    
    reject_comments.short_description = "Reject selected comments"

# Register models with the custom admin site
admin_site.register(Post, PostAdmin)
admin_site.register(PostCategory, PostCategoryAdmin)
admin_site.register(PostTag, PostTagAdmin)
admin_site.register(PostComment, PostCommentAdmin)