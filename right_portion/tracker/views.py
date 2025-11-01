from django.shortcuts import render
from .models import Food

def dashboard(request):
    foods = Food.objects.all # Food.objects.filter(user=request.user)
    return render(request, "tracker/dashboard.html", {"foods": foods})
