from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import secrets
import json
from .models import BlogPost, Category, Tag, PublicKeyUser
from .crypto_auth import (
    generate_key_pair, sign_message, get_public_key_fingerprint, 
    encrypt_fingerprint_and_hash, verify_encrypted_fingerprint_and_hash
)


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
    return render(request, 'blog/post_list.html', context)


def post_detail(request: HttpRequest, slug: str):
    """Display a single blog post"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    related_posts = BlogPost.objects.filter(
        published=True,
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Verify encryption if post has encrypted data and author_user exists
    if post.encrypted_data and post.author_user:
        from .crypto_auth import verify_encrypted_fingerprint_and_hash
        encrypted_valid = verify_encrypted_fingerprint_and_hash(
            post.author_user.public_key,
            post.encrypted_data,
            post.author_user.fingerprint,
            post.content
        )
        
        # Update encrypted_valid if it changed
        if post.encrypted_valid != encrypted_valid:
            post.encrypted_valid = encrypted_valid
            post.save(update_fields=['encrypted_valid'])
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)


def category_detail(request: HttpRequest, slug: str):
    """Display posts in a category"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, published=True).order_by('-created_at')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_detail.html', context)


def generate_keys(request: HttpRequest):
    """Generate a new key pair and return private key as downloadable file"""
    private_key, public_key = generate_key_pair()
    
    # Create HTTP response with file download
    from django.http import HttpResponse
    response = HttpResponse(private_key, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="private_key.pem"'
    return response


@require_http_methods(["POST"])
def auth_login(request: HttpRequest):
    """Authenticate user using uploaded private key file"""
    try:
        # Get uploaded file
        if 'private_key_file' not in request.FILES:
            return JsonResponse({'error': 'No private key file uploaded'}, status=400)
        
        private_key_file = request.FILES['private_key_file']
        private_key_pem = private_key_file.read().decode('utf-8')
        
        # Extract public key from private key
        from .crypto_auth import extract_public_key_from_private, sign_message
        public_key = extract_public_key_from_private(private_key_pem)
        
        # Get challenge from form data or session
        challenge = request.POST.get('challenge') or request.session.get('auth_challenge')
        if not challenge:
            # Generate a new challenge
            challenge = secrets.token_urlsafe(32)
            request.session['auth_challenge'] = challenge
        
        # Sign challenge with private key
        signature = sign_message(private_key_pem, challenge)
        
        # Authenticate user
        from django.contrib.auth import authenticate
        user = authenticate(
            request=request,
            public_key_pem=public_key,
            signature=signature,
            challenge=challenge
        )
        
        if user:
            # Clear challenge from session
            if 'auth_challenge' in request.session:
                del request.session['auth_challenge']
            # Log the user in
            login(request, user)
            return JsonResponse({
                'success': True,
                'user': {
                    'fingerprint': user.get_short_fingerprint(),
                }
            })
        else:
            return JsonResponse({'error': 'Invalid private key or signature'}, status=401)
            
    except UnicodeDecodeError:
        return JsonResponse({'error': 'Invalid file format. Please upload a valid private key file.'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({'error': f'Login error: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_challenge(request: HttpRequest):
    """Get a challenge string for authentication"""
    challenge = secrets.token_urlsafe(32)
    request.session['auth_challenge'] = challenge
    return JsonResponse({'challenge': challenge})


def login_page(request: HttpRequest):
    """Display login page"""
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    
    return render(request, 'blog/login.html')


def user_profile(request: HttpRequest):
    """Display user profile with public key"""
    # Check if viewing own profile or another user's profile
    fingerprint = request.GET.get('user')
    
    if fingerprint:
        # Viewing another user's profile
        try:
            user = PublicKeyUser.objects.get(fingerprint=fingerprint)
            is_own_profile = request.user.is_authenticated and request.user.id == user.id
        except PublicKeyUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('blog:post_list')
    else:
        # Viewing own profile
        if not request.user.is_authenticated:
            messages.info(request, 'Please login to view your profile.')
            return redirect('blog:login_page')
        user = request.user
        is_own_profile = True
    
    user_posts = BlogPost.objects.filter(author_user=user).order_by('-created_at')
    
    context = {
        'user': user,
        'posts': user_posts,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'blog/profile.html', context)


@require_http_methods(["POST"])
def auth_logout(request: HttpRequest):
    """Logout user and clear all cookies"""
    # Logout user (clears session)
    if request.user.is_authenticated:
        logout(request)
    
    # Flush session data
    request.session.flush()
    
    # Create response and clear all cookies
    response = redirect('blog:post_list')
    
    # Clear session cookie
    response.delete_cookie('sessionid', path='/')
    response.delete_cookie('csrftoken', path='/')
    
    # Clear any other cookies that might exist
    for cookie_name in request.COOKIES:
        response.delete_cookie(cookie_name, path='/')
    
    messages.success(request, 'You have been logged out successfully.')
    return response


@require_http_methods(["GET", "POST"])
def post_create(request: HttpRequest):
    """Create a new blog post - requires authentication"""
    # Check authentication
    if not request.user.is_authenticated:
        messages.info(request, 'Please login with your private key to create posts.')
        return redirect('blog:login_page')
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        # Author is set to user's fingerprint (from hidden field)
        author = request.POST.get('author', '').strip()
        if not author and request.user.is_authenticated:
            author = request.user.get_short_fingerprint()
        if not author:
            author = 'Anonymous'
        category_id = request.POST.get('category')
        new_category_name = request.POST.get('new_category', '').strip()
        tag_ids = request.POST.getlist('tags')
        new_tags_string = request.POST.get('new_tags', '').strip()
        published = request.POST.get('published') == 'on'
        
        if not title or not content:
            messages.error(request, 'Title and content are required')
            return redirect('blog:post_create')
        
        # Generate slug from title
        slug = slugify(title)
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Create post without encryption requirement
        post = BlogPost(
            title=title,
            slug=slug,
            content=content,
            excerpt=excerpt,
            author=author,
            published=published,
            author_user=request.user if request.user.is_authenticated else None,
            encrypted_data='',  # No encryption required
            encrypted_valid=False
        )
        
        # Handle category - prioritize new category name over existing selection
        if new_category_name:
            # Create or get category by name
            category_slug = slugify(new_category_name)
            category, created = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': new_category_name}
            )
            post.category = category
        elif category_id:
            try:
                post.category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        
        post.save()
        
        # Add existing tags
        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
                post.tags.add(tag)
            except Tag.DoesNotExist:
                pass
        
        # Create and add new tags
        if new_tags_string:
            tag_names = [name.strip() for name in new_tags_string.split(',') if name.strip()]
            for tag_name in tag_names:
                if tag_name:  # Ensure tag name is not empty
                    tag_slug = slugify(tag_name)
                    tag, created = Tag.objects.get_or_create(
                        slug=tag_slug,
                        defaults={'name': tag_name}
                    )
                    post.tags.add(tag)
        
        messages.success(request, 'Post created successfully!')
        return redirect('blog:post_detail', slug=post.slug)
    
    # GET request - show form
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/post_create.html', context)


@require_http_methods(["POST"])
def api_create_post(request: HttpRequest):
    """API endpoint to create a post via AJAX - requires authentication"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    excerpt = request.POST.get('excerpt', '').strip()
    # Author is set to user's fingerprint (from hidden field)
    author = request.POST.get('author', '').strip()
    if not author and request.user.is_authenticated:
        author = request.user.get_short_fingerprint()
    if not author:
        author = 'Anonymous'
    category_id = request.POST.get('category')
    new_category_name = request.POST.get('new_category', '').strip()
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
    
    # Create post without encryption requirement
    post = BlogPost(
        title=title,
        slug=slug,
        content=content,
        excerpt=excerpt,
        author=author,
        published=published,
        author_user=request.user if request.user.is_authenticated else None,
        encrypted_data='',  # No encryption required
        encrypted_valid=False
    )
    
    # Handle category - prioritize new category name over existing selection
    if new_category_name:
        # Create or get category by name
        category_slug = slugify(new_category_name)
        category, created = Category.objects.get_or_create(
            slug=category_slug,
            defaults={'name': new_category_name}
        )
        post.category = category
    elif category_id:
        try:
            post.category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass
    
    post.save()
    
    # Add existing tags
    for tag_id in tag_ids:
        try:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        except Tag.DoesNotExist:
            pass
    
    # Create and add new tags
    if new_tags_string:
        tag_names = [name.strip() for name in new_tags_string.split(',') if name.strip()]
        for tag_name in tag_names:
            if tag_name:  # Ensure tag name is not empty
                tag_slug = slugify(tag_name)
                tag, created = Tag.objects.get_or_create(
                    slug=tag_slug,
                    defaults={'name': tag_name}
                )
                post.tags.add(tag)
    
    return JsonResponse({
        'post': {
            'id': post.id,
            'title': post.title,
            'slug': post.slug,
            'url': post.get_absolute_url(),
        }
    }, status=201)
