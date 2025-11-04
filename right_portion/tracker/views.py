from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Meal, MealFood, Food
from .forms import MealForm, MealFoodFormSet, FoodForm

def dashboard(request):
    foods = Food.objects.all # Food.objects.filter(user=request.user)
    meals = Meal.objects.all
    return render(request, "tracker/dashboard.html", {"foods": foods, "meals": meals})


@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        formset = MealFoodFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            formset.instance = meal
            formset.save()
            return redirect("dashboard")

            # meal_foods = formset.save(commit=False)
            # for mf in meal_foods:
            #     mf.meal = meal
            #     mf.save()

            # return redirect("tracker:meal_list")

    else:
        form = MealForm()
        formset = MealFoodFormSet()

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'tracker/add_meal.html', context)


@login_required
def edit_meal(request, meal_slug):
    meal = Meal.objects.get(slug=meal_slug)

    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        formset = MealFoodFormSet(request.POST, instance=meal)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("dashboard")
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)


    else:
        form = MealForm(instance=meal)
        formset = MealFoodFormSet(instance=meal)

    context = {
        'form': form,
        'formset': formset,
        'meal': meal,
    }

    return render(request, 'tracker/meal-edit-page.html', context)


@login_required
def delete_meal(request, meal_slug):
    meal = Meal.objects.filter(slug=meal_slug)

    if request.method == 'POST':
        meal.delete()
        return redirect('dashboard')

    return render(request, 'tracker/meal-delete-page.html', {'meal': meal})



@login_required
def add_food(request):
    form = FoodForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        food = form.save(commit=False)
        food.user = request.user
        food.save()
        return redirect('dashboard')
    return render(request, 'tracker/food-add-page.html', {"form": form})


@login_required
def edit_food(request, food_slug):
    food = Food.objects.get(slug=food_slug)

    if request.method == "GET":
        form = FoodForm(instance=food, initial=food.__dict__)
    else:
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(request, 'tracker/food-edit-page.html', {"form": form})


@login_required
def delete_food(request, food_slug):
    food = Food.objects.filter(slug=food_slug)

    if request.method == 'POST':
        food.delete()
        return redirect('dashboard')

    return render(request, 'tracker/food-delete-page.html', {'food': food})

