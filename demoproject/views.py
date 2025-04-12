from django.shortcuts    import render;
from django.http          import HttpResponse;

def home(request):
    return render(request, 'welcome.html');

def about(request):
    return render(request, 'demo.html', )

def demo(request):
    return render(request, 'demo.html', {'title': 'Demo view'});
