from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Meal, MealFood, Food
from .forms import MealForm, MealFoodFormSet

@login_required
def dashboard(request):
    foods = Food.objects.all # Food.objects.filter(user=request.user)
    meals = Meal.objects.all
    return render(request, "tracker/dashboard.html", {"foods": foods, "meals": meals})


@login_required
def add_meal(request):
    if request.method == 'POST':
        meal_form = MealForm(request.POST)
        formset = MealFoodFormSet(request.POST)

        if meal_form.is_valid() and formset.is_valid():
            meal = meal_form.save(commit=False)
            meal.user = request.user
            meal.save()
            formset.instance = meal
            formset.save()
            return redirect("tracker:meal_list")

            # meal_foods = formset.save(commit=False)
            # for mf in meal_foods:
            #     mf.meal = meal
            #     mf.save()

            # return redirect("tracker:meal_list")

    else:
        meal_form = MealForm()
        formset = MealFoodFormSet()

    return render(request, 'tracker/add_meal.html', {
        'meal_form': meal_form,
        'formset': formset,
    })
