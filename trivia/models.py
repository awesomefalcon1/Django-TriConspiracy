from django.db import models
from django.utils import timezone
from django.urls import reverse


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
        return reverse('trivia:category_detail', kwargs={'slug': self.slug})


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    published = models.BooleanField(default=False, help_text='Only published posts are visible to visitors')
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
        return reverse('trivia:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
