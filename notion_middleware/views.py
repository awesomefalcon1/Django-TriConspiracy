from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from .models import Event, Question, Prize, Placement
from .notion_client import NotionClient


def event_list(request: HttpRequest):
    # Prefer Notion as the source of truth
    try:
        client = NotionClient()
        events = client.list_events()
    except Exception:
        # Fallback to local DB if Notion is not configured
        events = [
            {
                'id': str(ev.id),
                'title': ev.title,
                'description': ev.description,
                'location': ev.location,
                'starts_at': ev.starts_at.isoformat(),
            }
            for ev in Event.objects.order_by('-starts_at')
        ]
    return render(request, 'notion_middleware/event_list.html', {'events': events})


def event_detail(request: HttpRequest, event_id: str):
    try:
        client = NotionClient()
        event = client.get_event(event_id)
        questions = client.list_questions(event_id)
        prizes = client.list_prizes(event_id)
        placements = client.list_placements(event_id)
    except Exception:
        # Fallback to local DB id
        ev = get_object_or_404(Event, id=event_id)
        event = {
            'id': str(ev.id),
            'title': ev.title,
            'description': ev.description,
            'location': ev.location,
            'starts_at': ev.starts_at.isoformat(),
        }
        questions = list(ev.questions.all())
        prizes = list(ev.prizes.all())
        placements = list(ev.placements.all())
    return render(request, 'notion_middleware/event_detail.html', {'event': event, 'questions': questions, 'prizes': prizes, 'placements': placements})


@require_http_methods(["POST"])
def api_create_event(request: HttpRequest):
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    starts_at = request.POST.get('starts_at', '').strip()
    location = request.POST.get('location', '').strip()

    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)

    try:
        client = NotionClient()
        event = client.create_event(title, description, starts_at or None, location)
        return JsonResponse({'event': event}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_create_question(request: HttpRequest):
    event_id = request.POST.get('event_id')
    text = request.POST.get('text', '').strip()
    choice_a = request.POST.get('choice_a', '').strip()
    choice_b = request.POST.get('choice_b', '').strip()
    choice_c = request.POST.get('choice_c', '').strip()
    choice_d = request.POST.get('choice_d', '').strip()
    correct_choice = request.POST.get('correct_choice', 'A').strip().upper()

    if not (event_id and text and choice_a and choice_b):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        client = NotionClient()
        q = client.create_question(event_id, text, choice_a, choice_b, choice_c, choice_d, correct_choice)
        return JsonResponse({'question': q}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_create_prize(request: HttpRequest):
    event_id = request.POST.get('event_id')
    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    rank = request.POST.get('rank')
    value = request.POST.get('value', '0')

    if not (event_id and name and rank):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        client = NotionClient()
        p = client.create_prize(event_id, name, description, int(rank), value)
        return JsonResponse({'prize': p}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_create_placement(request: HttpRequest):
    event_id = request.POST.get('event_id')
    participant_name = request.POST.get('participant_name', '').strip()
    score = request.POST.get('score', '0')
    rank = request.POST.get('rank')

    if not (event_id and participant_name and rank):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        client = NotionClient()
        pl = client.create_placement(event_id, participant_name, int(score or 0), int(rank))
        return JsonResponse({'placement': pl}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create your views here.
