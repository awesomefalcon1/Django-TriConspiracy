from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
from django.contrib import messages
from .models import BlogPost, Category, Tag


def post_list(request: HttpRequest):
    """Display list of published blog posts"""
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)
    
    # Filter by tag if provided
    tag_slug = request.GET.get('tag')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=tag)
    
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
    }
    return render(request, 'trivia/post_list.html', context)


def post_detail(request: HttpRequest, slug: str):
    """Display a single blog post"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    related_posts = BlogPost.objects.filter(
        published=True,
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'trivia/post_detail.html', context)


def category_detail(request: HttpRequest, slug: str):
    """Display posts in a category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, published=True).order_by('-created_at')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'trivia/category_detail.html', context)


@require_http_methods(["GET", "POST"])
def post_create(request: HttpRequest):
    """Create a new blog post"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        author = request.POST.get('author', 'Anonymous').strip()
        category_id = request.POST.get('category')
        tag_ids = request.POST.getlist('tags')
        published = request.POST.get('published') == 'on'
        
        if not title or not content:
            messages.error(request, 'Title and content are required')
            return redirect('trivia:post_create')
        
        # Generate slug from title
        slug = slugify(title)
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            author=author,
            published=published
        )
        
        if category_id:
            try:
                post.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        
        post.save()
        
        # Add tags
        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
                post.tags.add(tag)
            except Tag.DoesNotExist:
                pass
        
        messages.success(request, 'Post created successfully!')
        return redirect('trivia:post_detail', slug=post.slug)
    
    # GET request - show form
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'trivia/post_create.html', context)


@require_http_methods(["POST"])
def api_create_post(request: HttpRequest):
    """API endpoint to create a post via AJAX"""
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    excerpt = request.POST.get('excerpt', '').strip()
    author = request.POST.get('author', 'Anonymous').strip()
    category_id = request.POST.get('category')
    tag_ids = request.POST.getlist('tags')
    published = request.POST.get('published') == 'true'
    
    if not title or not content:
        return JsonResponse({'error': 'Title and content are required'}, status=400)
    
    # Generate slug
    slug = slugify(title)
    base_slug = slug
    counter = 1
    while BlogPost.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    post = BlogPost(
        title=title,
        slug=slug,
        content=content,
        excerpt=excerpt,
        author=author,
        published=published
    )
    
    if category_id:
        try:
            post.category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass
    
    post.save()
    
    # Add tags
    for tag_id in tag_ids:
        try:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        except Tag.DoesNotExist:
            pass
    
    return JsonResponse({
        'post': {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'url': post.get_absolute_url(),
        }
    }, status=201)
