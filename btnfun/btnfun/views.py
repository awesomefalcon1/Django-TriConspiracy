# views.py
from django.http import JsonResponse

def increment(request):
    ''''''
    number = request.session.get('number', 0)
    number += 1
    request.session['number'] = number
    return JsonResponse({'number': number})
# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
