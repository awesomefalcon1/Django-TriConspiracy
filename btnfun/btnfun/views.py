# views.py
from django.http import JsonResponse

def increment(request):
    ''''''
    number = request.session.get('number')
    number += 1
    request.session['number'] = number
    return JsonResponse({'number': number})
# views.py
from django.shortcuts import render

def index(request):
    number = request.session.get('number')
    return render(request, 'index.html', {'number': number})
