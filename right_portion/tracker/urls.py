from django.urls import path
from . import views

urlpatterns = [
    path('add_meal/', views.add_meal, name='add meal'),
    path('edit/<slug:meal_slug>/', views.edit_meal, name="meal edit"),
    path('delete/<slug:meal_slug>/', views.delete_meal, name="meal delete"),

    path('add_food/', views.add_food, name="add food"),
    path('edit/f/<slug:food_slug>/', views.edit_food, name="food edit"),
    path('delete/f/<slug:food_slug>/', views.delete_food, name="food delete"),
]