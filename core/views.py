from django.shortcuts import render

def index(request):
    """Main index page view"""
    return render(request, 'index.html')

def about(request):
    """About page view"""
    return render(request, 'about.html')

def contact(request):
    """Contact page view"""
    return render(request, 'contact.html')
