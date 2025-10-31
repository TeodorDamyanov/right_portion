from django.shortcuts import render
from django.http import HttpResponse

def account(request):
    return HttpResponse("Hello, Django!")