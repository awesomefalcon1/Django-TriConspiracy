from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text='Short summary of the post')
    author = models.CharField(max_length=100, default='Anonymous')
    author_user = models.ForeignKey('PublicKeyUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', help_text='Authenticated user who created this post')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    published = models.BooleanField(default=False, help_text='Only published posts are visible to visitors')
    encrypted_data = models.TextField(blank=True, help_text='Encrypted fingerprint and content hash')
    encrypted_valid = models.BooleanField(default=False, help_text='Whether the encryption has been verified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, help_text='Publication date')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class PublicKeyUserManager(BaseUserManager):
    """Manager for PublicKeyUser"""
    
    def create_user(self, public_key_pem):
        """Create a new user with a public key"""
        if not public_key_pem:
            raise ValueError('Users must have a public key')
        
        user = self.model(public_key=public_key_pem)
        user.last_login = timezone.now()
        user.save(using=self._db)
        return user


class PublicKeyUser(AbstractBaseUser):
    """
    Custom user model that authenticates using public/private key pairs.
    The private key is never stored - only the public key.
    """
    public_key = models.TextField(unique=True, help_text='Public key in PEM format')
    fingerprint = models.CharField(max_length=64, unique=True, help_text='SHA256 hash of public key')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'public_key'
    REQUIRED_FIELDS = []
    
    objects = PublicKeyUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['fingerprint']),
            models.Index(fields=['last_login']),
        ]
    
    def __str__(self):
        return f"User {self.fingerprint[:16] if self.fingerprint else 'Unknown'}"
    
    def get_short_fingerprint(self):
        """Get a short version of the fingerprint for display"""
        return self.fingerprint[:16] if self.fingerprint else 'Unknown'
    
    def save(self, *args, **kwargs):
        """Calculate fingerprint from public key if not set"""
        if self.public_key and not self.fingerprint:
            import hashlib
            self.fingerprint = hashlib.sha256(self.public_key.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
    
    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])
    
    def is_inactive(self, days=60):
        """Check if user hasn't logged in for specified days"""
        if not self.last_login:
            return True
        cutoff = timezone.now() - timedelta(days=days)
        return self.last_login < cutoff
