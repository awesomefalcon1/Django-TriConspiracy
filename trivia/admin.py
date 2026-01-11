from django.contrib import admin
from .models import BlogPost, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Metadata', {
            'fields': ('author', 'category', 'tags', 'published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
