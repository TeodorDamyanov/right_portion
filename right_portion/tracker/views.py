from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Meal, MealFood, Food, MealTemplate, MealTemplateFood, Plan
from .forms import MealForm, MealFoodFormSet, FoodForm

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

    else:
        form = MealForm()
        formset = MealFoodFormSet()

        for f in formset.forms:
            f.fields['food'].queryset = Food.objects.order_by('-is_favorite', 'name')

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'tracker/meal/add_meal.html', context)

@login_required
def food_details(request, food_slug):
    food = Food.objects.filter(slug=food_slug).first()

    context = {
        "food": food,
    }

    return render(request, 'tracker/food/food-details-page.html', context)


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

    return render(request, 'tracker/meal/meal-edit-page.html', context)


@login_required
def delete_meal(request, meal_slug):
    meal = Meal.objects.filter(slug=meal_slug)

    if request.method == 'POST':
        meal.delete()
        return redirect('dashboard')

    return render(request, 'tracker/meal/meal-delete-page.html', {'meal': meal})



@login_required
def add_food(request):
    form = FoodForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        food = form.save(commit=False)
        food.user = request.user
        food.save()
        next_url = request.GET.get('next', 'dashboard')
        return redirect(next_url)
    return render(request, 'tracker/food/add_food.html', {"form": form})


@login_required
def edit_food(request, food_slug):
    food = Food.objects.get(slug=food_slug)

    if request.method == "GET":
        form = FoodForm(instance=food, initial=food.__dict__)
    else:
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)

    return render(request, 'tracker/food/food-edit-page.html', {"form": form})


@login_required
def delete_food(request, food_slug):
    food = Food.objects.filter(slug=food_slug)

    if request.method == 'POST':
        food.delete()
        return redirect('dashboard')

    return render(request, 'tracker/food/food-delete-page.html', {'food': food})


@login_required
def save_meal_as_template(request, meal_slug):
    meal = Meal.objects.get(slug=meal_slug)

    template = MealTemplate.objects.create(user=request.user, name=meal.name)

    for meal_food in meal.meal_foods.all():
        MealTemplateFood.objects.create(
            meal_template=template,
            food=meal_food.food,
            quantity=meal_food.quantity
        )

    return redirect('dashboard')

@login_required
def add_meal_from_template(request, template_id):
    template = MealTemplate.objects.get(id=template_id, user=request.user)

    if request.method == "POST":
        meal = Meal(
            user=request.user,
            name=template.name,
            date=timezone.now().date()
        )
        
        meal.pk = None
        meal.id = None
        meal.save()

        for t_food in template.template_foods.all():
            MealFood.objects.create(
            meal=meal,
            food=t_food.food,
            quantity=t_food.quantity
        )

    return redirect('dashboard')


@login_required
def meal_templates(request):
    templates = MealTemplate.objects.filter(user=request.user)
    show_favorites = request.GET.get("favorites")
    
    if show_favorites:
        templates = templates.filter(is_favorite=True)
    return render(request, 'tracker/meal/meal_templates.html', {'templates': templates})


@login_required
def toggle_favorite(request, template_id):
    template = MealTemplate.objects.get(id=template_id, user=request.user)
    template.is_favorite = not template.is_favorite
    template.save()
    return redirect('templates')


@login_required
def toggle_favorite_food(request, food_id):
    food = Food.objects.get(id=food_id, user=request.user)
    food.is_favorite = not food.is_favorite
    food.save()
    return redirect(request.META.get('HTTP_REFERER', 'food_list'))


@login_required
def delete_meal_template(request, template_id):
    template = MealTemplate.objects.filter(id=template_id).first()
    if request.method == 'POST':
        template.delete()
        return redirect('templates')

    return render(request, 'tracker/meal/meal-template-delete-page.html', {'template': template})