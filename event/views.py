from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Home Page")

def show_event(request):
    return HttpResponse("Events")

def dashboard(request):
    return render(request,"dashboard.html")