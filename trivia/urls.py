from django.urls import path
from . import views


app_name = 'trivia'


urlpatterns = [
    # Blog post views
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # API endpoints
    path('api/posts/', views.api_create_post, name='api_create_post'),
]

