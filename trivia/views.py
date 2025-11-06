from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from django.utils.dateparse import parse_datetime
from .models import Event, Question, Prize, Placement


def event_list(request: HttpRequest):
    events = Event.objects.order_by('-starts_at')
    return render(request, 'trivia/event_list.html', {'events': events})


def event_detail(request: HttpRequest, event_id: int):
    ev = get_object_or_404(Event, id=event_id)
    questions = ev.questions.all()
    prizes = ev.prizes.all()
    placements = ev.placements.all()
    return render(request, 'trivia/event_detail.html', {'event': ev, 'questions': questions, 'prizes': prizes, 'placements': placements})


@require_http_methods(["POST"])
def api_create_event(request: HttpRequest):
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    starts_at = request.POST.get('starts_at', '').strip()
    location = request.POST.get('location', '').strip()

    if not title:
        return JsonResponse({'error': 'Title is required'}, status=400)

    event = Event(title=title, description=description, location=location)
    if starts_at:
        try:
            parsed = parse_datetime(starts_at)
            if parsed:
                event.starts_at = parsed
        except Exception:
            pass
    event.save()
    return JsonResponse({'event': model_to_dict(event)}, status=201)


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

    event = get_object_or_404(Event, id=event_id)
    question = Question(
        event=event,
        text=text,
        choice_a=choice_a,
        choice_b=choice_b,
        choice_c=choice_c,
        choice_d=choice_d,
        correct_choice=correct_choice or 'A',
    )
    question.save()
    return JsonResponse({'question': model_to_dict(question)}, status=201)


@require_http_methods(["POST"])
def api_create_prize(request: HttpRequest):
    event_id = request.POST.get('event_id')
    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()
    rank = request.POST.get('rank')
    value = request.POST.get('value', '0')

    if not (event_id and name and rank):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    event = get_object_or_404(Event, id=event_id)
    prize = Prize(event=event, name=name, description=description, rank=int(rank), value=value)
    prize.save()
    return JsonResponse({'prize': model_to_dict(prize)}, status=201)


@require_http_methods(["POST"])
def api_create_placement(request: HttpRequest):
    event_id = request.POST.get('event_id')
    participant_name = request.POST.get('participant_name', '').strip()
    score = request.POST.get('score', '0')
    rank = request.POST.get('rank')

    if not (event_id and participant_name and rank):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    event = get_object_or_404(Event, id=event_id)
    placement = Placement(event=event, participant_name=participant_name, score=int(score or 0), rank=int(rank))
    placement.save()
    return JsonResponse({'placement': model_to_dict(placement)}, status=201)

# Create your views here.
