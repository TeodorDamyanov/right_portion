from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.db.models import F, Sum, FloatField, ExpressionWrapper
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from right_portion.tracker.models import Meal, MealFood, Plan

@login_required
def dashboard(request):
    today = timezone.localdate()
    print(today)
    week_ago = today - timedelta(days=6)
    recent_meals = Meal.objects.filter(user=request.user, date__range=[week_ago, today])

    meals = Meal.objects.filter(user=request.user, date=today)
    plan = Plan.objects.filter(user=request.user).first()

    meals_by_day = (
        recent_meals
        .values("date")
        .annotate(
            total_calories=Sum(
                ExpressionWrapper(
                    F("meal_foods__quantity") * F("meal_foods__food__calories") / 100,
                    output_field=FloatField(),
                )
            )
        )
    )

    if meals_by_day:
        avg_calories = sum(m['total_calories'] for m in meals_by_day) / len(meals_by_day)
    else:
        avg_calories = 0

    streak = 0
    day = today
    while Meal.objects.filter(user=request.user, date=day).exists():
        streak += 1
        day -= timedelta(days=1)


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

        "avg_calories": round(avg_calories),
        "streak": streak,

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
def history(request):
    user = request.user
    meals = Meal.objects.filter(user=user).order_by("-date")

    daily_data = defaultdict(int)
    for meal in meals:
        daily_data[meal.date] += meal.total_calories

    daily_data = [
        {"date": day, "total_calories": total}
        for day, total in sorted(daily_data.items(), reverse=True)
    ]

    daily_data = (
        Meal.objects.filter(user=user)
        .values("date")
        .annotate(
            total_calories=Sum(
                ExpressionWrapper(
                    F("meal_foods__quantity") * F("meal_foods__food__calories") / 100,
                    output_field=FloatField(),
                )
            )
        )
        .order_by("-date")
    )

    return render(request, "tracker/history.html", {
        "daily_data": daily_data,
    })


@login_required
def day_history(request, day):
    user = request.user
    meals = Meal.objects.filter(user=user, date=day).order_by("-id")
    return render(request, "tracker/day_history.html", {
        "meals": meals,
        "day": day,
    })