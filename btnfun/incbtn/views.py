from django.shortcuts import render

# Create your views here.
# views.py
from django.http import JsonResponse
from .models import Number
def increment(request):
    number, created = Number.objects.get_or_create(pk=1)
    number.value += 1
    number.save()
    return JsonResponse({'number': number.value})
# views.py
from django.shortcuts import render

def index(request):
    number, created = Number.objects.get_or_create(pk=1)
    number = number.value
    if number is None:
        number = 0
    return render(request, 'index.html', {'number': number})
