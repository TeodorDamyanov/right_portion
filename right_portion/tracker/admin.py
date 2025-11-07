from django.contrib import admin
from .models import Food, Meal, Plan

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein',)
    search_fields = ['name']

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)
    search_fields = ['name']
    
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'num_days', 'daily_calories')
    search_fields = ['user']

@admin.register(Plan)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ['name']