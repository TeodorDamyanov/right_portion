from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from right_portion.tracker.models import Meal, MealFood, Plan

@login_required
def dashboard(request):
    today = timezone.localdate()
    meals = Meal.objects.filter(user=request.user, date=today)
    plan = Plan.objects.filter(user=request.user).first()


    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0

    for meal in meals:
        for meal_food in meal.meal_foods.all():
            total_calories += meal_food.total_calories
            total_protein += meal_food.total_protein
            total_carbs += meal_food.total_carbs
            total_fats += meal_food.total_fats

    def percent(current, goal):
        return round((current / goal) * 100, 1)

    context = {
        'meals': meals,
        'plan': plan,
        'total_calories': round(total_calories, 1),
        'total_protein': round(total_protein, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fats': round(total_fats, 1),

        'calories_percent': percent(total_calories, plan.daily_calories),
        'protein_percent': percent(total_protein, plan.protein_goal),
        'carbs_percent': percent(total_carbs, plan.carbs_goal),
        'fats_percent': percent(total_fats, plan.fats_goal),
    }
    return render(request, 'tracker/dashboard.html', context)


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base/welcome.html')


@login_required
def meal_history(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date')
    selected_date = request.GET.get('date')
    if selected_date:
        meals = meals.filter(date=selected_date)


    history = {}
    for meal in meals:
        history.setdefault(meal.date, []).append(meal)

    context = {
        'history': history,
    }
    return render(request, 'tracker/meal/meal-history-page.html', context)