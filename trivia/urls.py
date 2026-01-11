from django.urls import path
from . import views


app_name = 'trivia'


urlpatterns = [
    # Blog post views
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Authentication endpoints
    path('api/generate-keys/', views.generate_keys, name='generate_keys'),
    path('api/get-challenge/', views.get_challenge, name='get_challenge'),
    path('api/login/', views.auth_login, name='auth_login'),
    
    # API endpoints
    path('api/posts/', views.api_create_post, name='api_create_post'),
]

