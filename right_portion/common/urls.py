from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meal-history/', views.meal_history, name='meal history'),
    path('', views.index, name='index'),
]