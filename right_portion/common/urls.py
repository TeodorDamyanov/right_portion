from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("history/", views.history, name="history"),
    path("history/<str:day>/", views.day_history, name="day_history"),
    path('', views.index, name='index'),
]