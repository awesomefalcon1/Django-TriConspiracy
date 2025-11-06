from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from main.constants import settings
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
# from main.engines import ContentEngine, GGUFContentEngine, LLMContentEngine, LargeFeatureExtractionEngine

content_engine = None
large_feature_extraction_engine = None
GGUF_content_engine = None

def token_auth(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('X-API-TOKEN') != settings.Constants.API_TOKEN:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
@require_POST
@token_auth
def predict(request):
    item = request.POST.get('item')
    num_predictions = int(request.POST.get('num', 10))
    if not item:
        return JsonResponse([], safe=False)
    if content_engine is None:
        content_engine = ContentEngine()
    predictions = content_engine.predict(str(item), num_predictions)
    predictions = [(p[0].decode('utf-8'), float(p[1])) for p in predictions]
    return JsonResponse(predictions, safe=False)

@csrf_exempt
@token_auth
def train(request):
    data_url = request.POST.get('data-url')
    if content_engine is None:
        content_engine = ContentEngine()
    content_engine.train(data_url)
    return JsonResponse({"message": "Success!", "success": 1})

@csrf_exempt
@token_auth
def feature_extraction(request):
    text = request.POST.get('text')
    if content_engine is None:
        content_engine = ContentEngine()
    return JsonResponse({"embedding": content_engine.feature_extraction(text)})

@csrf_exempt
@token_auth
def sentence_similarity(request):
    text1 = request.POST.get('text1')
    text2 = request.POST.get('text2')
    if content_engine is None:
        content_engine = ContentEngine()
    return JsonResponse({"similarity": content_engine.sentence_similarity(text1, text2)})

@csrf_exempt
@token_auth
def fetch_large_feature_extraction_engine(request):
    model_name = request.POST.get('model-name')
    if large_feature_extraction_engine is None:
        large_feature_extraction_engine = LargeFeatureExtractionEngine(model_name)
    return JsonResponse({"success": 1, "loaded_model": model_name})

@csrf_exempt
@token_auth
def extract_features_with_large_feature_extraction_engine(request):
    text = request.POST.get('text')
    if large_feature_extraction_engine is None:
        return JsonResponse({"error": "Large feature extraction engine not loaded"}, status=400)
    return JsonResponse({"embedding": large_feature_extraction_engine.extract_features(text)})

@csrf_exempt
@token_auth
def sentence_similarity_with_large_feature_extraction_engine(request):
    text1 = request.POST.get('text1')
    text2 = request.POST.get('text2')
    if large_feature_extraction_engine is None:
        return JsonResponse({"error": "Large feature extraction engine not loaded"}, status=400)
    return JsonResponse({"similarity": large_feature_extraction_engine.sentence_similarity(text1, text2)})

@csrf_exempt
@token_auth
def score_matrix_with_large_feature_extraction_engine(request):
    csv_path = request.POST.get('csv-path')
    sentence_col = request.POST.get('sentence-col')
    if large_feature_extraction_engine is None:
        return JsonResponse({"error": "Large feature extraction engine not loaded"}, status=400)
    return JsonResponse({"score_matrix": large_feature_extraction_engine.score_matrix(csv_path, sentence_col)})

@csrf_exempt
@token_auth
def csv_feature_extraction_with_large_feature_extraction_engine(request):
    csv_path = request.POST.get('csv-path')
    sentence_col = request.POST.get('sentence-col')
    if large_feature_extraction_engine is None:
        return JsonResponse({"error": "Large feature extraction engine not loaded"}, status=400)
    return JsonResponse({"embeddings": large_feature_extraction_engine.feature_extraction(csv_path, sentence_col)})

@csrf_exempt
@token_auth
def fetch_GGUF_embeddings_model(request):
    model_name = request.POST.get('model-name')
    if GGUF_content_engine is None:
        GGUF_content_engine = GGUFContentEngine()
    GGUF_content_engine.set_embedding_model(model_name)
    return JsonResponse({"success": 1, "loaded_model": model_name})

@csrf_exempt
@token_auth
def fetch_GGUF_chat_model(request):
    model_name = request.POST.get('model-name')
    if GGUF_content_engine is None:
        GGUF_content_engine = GGUFContentEngine()
    GGUF_content_engine.set_chat_model(model_name)
    return JsonResponse({"success": 1, "loaded_model": model_name})

@csrf_exempt
@token_auth
def extract_features_with_GGUF_engine(request):
    text = request.POST.get('text')
    if GGUF_content_engine is None:
        return JsonResponse({"error": "gguf engine not loaded"}, status=400)
    return JsonResponse({"embedding": GGUF_content_engine.extract_features(text)})

@csrf_exempt
@token_auth
def sentence_similarity_with_GGUF_engine(request):
    text1 = request.POST.get('text1')
    text2 = request.POST.get('text2')
    if GGUF_content_engine is None:
        return JsonResponse({"error": "gguf engine not loaded"}, status=400)
    return JsonResponse({"similarity": GGUF_content_engine.sentence_similarity(text1, text2)})

@csrf_exempt
@token_auth
def csv_feature_extraction_with_GGUF_engine(request):
    csv_path = request.POST.get('csv-path')
    sentence_col = request.POST.get('sentence-col')
    if GGUF_content_engine is None:
        return JsonResponse({"error": "gguf engine not loaded"}, status=400)
    return JsonResponse({"embeddings": GGUF_content_engine.feature_extraction(csv_path, sentence_col)})

@csrf_exempt
@token_auth
def score_matrix_with_GGUF_engine(request):
    csv_path = request.POST.get('csv-path')
    sentence_col = request.POST.get('sentence-col')
    if GGUF_content_engine is None:
        return JsonResponse({"error": "gguf engine not loaded"}, status=400)
    return JsonResponse({"score_matrix": GGUF_content_engine.score_matrix(csv_path, sentence_col)})


def train_ui(request):
    if request.method == 'POST':
        data_url = request.POST.get('data-url')
        if content_engine is None:
            content_engine = ContentEngine()
        content_engine.train(data_url)
        messages.success(request, 'Training started successfully')
        return redirect('train_ui')
    return render(request, 'train.html')

