from django.urls import path
from . import views


app_name = 'trivia'


urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    # API endpoints (AJAX)
    path('api/events/', views.api_create_event, name='api_create_event'),
    path('api/questions/', views.api_create_question, name='api_create_question'),
    path('api/prizes/', views.api_create_prize, name='api_create_prize'),
    path('api/placements/', views.api_create_placement, name='api_create_placement'),
]

