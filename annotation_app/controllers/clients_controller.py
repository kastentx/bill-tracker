from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def example_client(request):
  return render(request, 'example.html')

def megalith(request):
  return render(request, 'megalith/megalith.html')
