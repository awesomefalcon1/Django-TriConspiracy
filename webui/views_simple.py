from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from main.constants import settings
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages

def token_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('X-API-TOKEN') != settings.Constants.API_TOKEN:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    """Simple index page for webui"""
    return render(request, 'index.html')

@csrf_exempt
@token_auth
def predict(request):
    """Placeholder predict function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)

@csrf_exempt
@token_auth
def train(request):
    """Placeholder train function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)

@csrf_exempt
@token_auth
def feature_extraction(request):
    """Placeholder feature extraction function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)

@csrf_exempt
@token_auth
def sentence_similarity(request):
    """Placeholder sentence similarity function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)

@csrf_exempt
@token_auth
def csv_feature_extraction(request):
    """Placeholder CSV feature extraction function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)

@csrf_exempt
@token_auth
def score_matrix(request):
    """Placeholder score matrix function"""
    return JsonResponse({"message": "Engine not configured", "success": 0}, status=500)
