from django.urls import path
from . import views

urlpatterns = [
    path('add_meal/', views.add_meal, name='add meal'),
    path('edit/<slug:meal_slug>/', views.edit_meal, name="meal edit"),
    path('delete/<slug:meal_slug>/', views.delete_meal, name="meal delete"),

    path('add_food/', views.add_food, name="add food"),
    path('details/<slug:food_slug>/', views.food_details, name="food details"),
    path('edit/f/<slug:food_slug>/', views.edit_food, name="food edit"),
    path('delete/f/<slug:food_slug>/', views.delete_food, name="food delete"),

    path('meal/<slug:meal_slug>/save-template/', views.save_meal_as_template, name='save meal as template'),
    path('templates/', views.meal_templates, name='templates'),
    path('templates/add/<int:template_id>/', views.add_meal_from_template, name='add meal from template'),
    path("templates/<int:template_id>/favorite/", views.toggle_favorite, name="toggle favorite"),
    path('templates/delete/<int:template_id>/', views.delete_meal_template, name='delete meal template'),
]