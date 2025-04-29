from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, PostCategory, PostTag, PostComment

def blog_list(request):
    """View for listing all blog posts"""
    posts = Post.objects.filter(status='active')
    paginator = Paginator(posts, 9)  # 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'recent_posts': Post.objects.filter(status='active').order_by('-created_at')[:5],
        'categories': PostCategory.objects.filter(status=True),
        'tags': PostTag.objects.filter(status=True),
    }
    return render(request, 'blog/blog_list.html', context)

def post_detail(request, slug):
    """View for displaying a single blog post"""
    post = get_object_or_404(Post, slug=slug, status='active')
    comments = PostComment.objects.filter(post=post, status=True)
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')
        
        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(PostComment, id=parent_id)
        
        if comment_text:
            PostComment.objects.create(
                user=request.user,
                post=post,
                comment=comment_text,
                parent_comment=parent_comment
            )
    
    context = {
        'post': post,
        'comments': comments,
        'recent_posts': Post.objects.filter(status='active').exclude(id=post.id).order_by('-created_at')[:4],
        'related_posts': Post.objects.filter(post_cat=post.post_cat, status='active').exclude(id=post.id)[:3],
        'categories': PostCategory.objects.filter(status=True),
        'tags': PostTag.objects.filter(status=True),
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, category_slug):
    """View for listing posts by category"""
    category = get_object_or_404(PostCategory, slug=category_slug, status=True)
    posts = Post.objects.filter(post_cat=category, status='active')
    
    paginator = Paginator(posts, 9)  # 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
        'recent_posts': Post.objects.filter(status='active').order_by('-created_at')[:5],
        'categories': PostCategory.objects.filter(status=True),
        'tags': PostTag.objects.filter(status=True),
    }
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, tag_slug):
    """View for listing posts by tag"""
    tag = get_object_or_404(PostTag, slug=tag_slug, status=True)
    posts = Post.objects.filter(tags=tag, status='active')
    
    paginator = Paginator(posts, 9)  # 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': tag,
        'posts': posts,
        'recent_posts': Post.objects.filter(status='active').order_by('-created_at')[:5],
        'categories': PostCategory.objects.filter(status=True),
        'tags': PostTag.objects.filter(status=True),
    }
    return render(request, 'blog/tag_posts.html', context)