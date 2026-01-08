from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from right_portion.common.forms import SearchForm
from .models import Meal, MealFood, Food, MealTemplate, MealTemplateFood, Plan
from .forms import MealForm, FoodForm

from ..usda import fetch_usda_foods


@login_required
def add_meal(request):
    all_foods = Food.objects.filter(user=request.user).order_by('-is_favorite')
    recent_food = all_foods.order_by('-id').first()
    search_query = request.GET.get("search", "")
    meal_name = request.GET.get("name", "New Meal")
    
    search_form = SearchForm(request.GET or None)
    request.session.pop("search_result", None)

    if search_query and request.GET.get("srch_btn") == "":
        recent_food = ""
        all_foods = all_foods.filter(name__icontains=search_query)

    if search_query and request.GET.get("usda_srch_btn") == "":
        recent_food = ""
        usda_data = fetch_usda_foods(search_query)
        if usda_data:
            if isinstance(usda_data, list):
                usda_data = search_food(request, usda_data)
                usda_data = usda_data[:5]
                request.session["search_result"] = usda_data
                all_foods = []


    if request.method == "GET":
        form = MealForm(initial={"name": meal_name})
    else:
        form = MealForm(request.POST)

        if form.is_valid():
            selected_foods = {}
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    food_id = key.replace('quantity_', '')
                    try:
                        quantity = float(value) if value else 100.0
                    except (ValueError, TypeError):
                        quantity = 100.0
                    selected_foods[food_id] = quantity
            
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            for food_id, quantity in selected_foods.items():
                food = Food.objects.get(id=food_id)
                MealFood.objects.create(meal=meal, food=food, quantity=quantity)
            return redirect("dashboard")

    all_foods = all_foods[:5]
    context = {
        "all_foods": all_foods,
        "search_form": search_form,
        'form': form,
        "meal_name": meal_name,
        "recent_food": recent_food,
        "usda_results": request.session.get("search_result", []),
    }
    return render(request, 'tracker/meal/add_meal.html', context)


@login_required
def add_db_food(request, add_edit):
    idx = int(request.GET.get("idx", 0))
    data_list = request.session.get("search_result", [])

    if not data_list or idx >= len(data_list):
        return redirect("add meal")

    data = data_list[idx]

    food = Food(
        name=data["name"],
        calories=data["calories"],
        protein=data["protein"],
        carbs=data["carbs"],
        fats=data["fat"],
    )

    food.user = request.user
    food.save()

    request.session.pop("search_result", None)
    if add_edit == "add":
        return redirect("add meal")
    else:
        return redirect("dashboard")


@login_required
def edit_meal(request, meal_slug):
    meal = Meal.objects.get(slug=meal_slug)
    all_foods = Food.objects.filter(user=request.user).order_by('-is_favorite')
    recent_food = all_foods.order_by('-id').first()
    search_query = request.GET.get("search", "")
    search_form = SearchForm()

    form = MealForm(request.POST or None, instance=meal)

    search_form = SearchForm(request.GET or None)
    request.session.pop("search_result", None)

    if search_query and request.GET.get("srch_btn") == "":
        recent_food = ""
        all_foods = all_foods.filter(name__icontains=search_query)

    if search_query and request.GET.get("usda_srch_btn") == "":
        recent_food = ""
        usda_data = fetch_usda_foods(search_query)
        if usda_data:
            if isinstance(usda_data, list):
                usda_data = search_food(request, usda_data)
                usda_data = usda_data[:5]
                request.session["search_result"] = usda_data
                all_foods = []


    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)

        if form.is_valid():
            form.save()
            meal.meal_foods.all().delete()
            selected_foods = {}
            for key, value in request.POST.items():
                if key.startswith("quantity_"):
                    food_id = key.replace("quantity_", "")
                    try:
                        quantity = float(value) if value else 100.0
                    except (ValueError, TypeError):
                        quantity = 100.0
                    selected_foods[food_id] = quantity

            for food_id, quantity in selected_foods.items():
                food = Food.objects.get(id=food_id, user=request.user)
                MealFood.objects.create(meal=meal, food=food, quantity=quantity)

            return redirect("dashboard")
        
    meal_food_ids = set(meal.meal_foods.values_list("food_id", flat=True))

    all_foods = all_foods[:5]
    context = {
        "meal": meal,
        "form": form,
        "all_foods": all_foods,
        "search_form": search_form,
        "meal_food_ids": meal_food_ids,
        "recent_food": recent_food,
        "usda_results": request.session.get("search_result", []),
    }

    return render(request, "tracker/meal/meal-edit-page.html", context)


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
def food_details(request, food_slug):
    food = Food.objects.filter(slug=food_slug).first()

    context = {
        "food": food,
    }

    return render(request, 'tracker/food/food-details-page.html', context)


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


def search_food(request, usda_data):
    food_names = list(Food.objects.values_list('name', flat=True))
    for f in usda_data:
        if f['name'] in food_names:
            foods = Food.objects.filter(name=f['name'], user=request.user)
            for food in foods:
                if food.calories == int(f['calories']) and food.protein == int(f['protein']) and food.carbs == int(f['carbs']) and food.fats == int(f['fat']):
                    usda_data.remove(f)
    return usda_data

