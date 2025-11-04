from django.db import models
from django.utils.text import slugify
from right_portion import settings

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    calories = models.IntegerField(help_text="Per 100g")
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.calories} cals per 100g"
    

class Plan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    num_days = models.IntegerField()
    daily_calories = models.IntegerField()
    protein_goal = models.IntegerField()
    carbs_goal = models.IntegerField()
    fats_goal = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Plan - {self.daily_calories} kcal/day"


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.id}")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.date}) - {self.user.username}"
    
    @property
    def total_calories(self):
        return sum([mf.total_calories for mf in self.meal_foods.all()])

    @property
    def total_protein(self):
        return sum([mf.total_protein for mf in self.meal_foods.all()])

    @property
    def total_carbs(self):
        return sum([mf.total_carbs for mf in self.meal_foods.all()])

    @property
    def total_fats(self):
        return sum([mf.total_fats for mf in self.meal_foods.all()])


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="meal_foods")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="In grams")

    @property
    def total_calories(self):
        return round(self.food.calories * self.quantity / 100)
    
    @property
    def total_protein(self):
        return round(self.food.protein * self.quantity / 100)

    @property
    def total_carbs(self):
        return round(self.food.carbs * self.quantity / 100)

    @property
    def total_fats(self):
        return round(self.food.fats * self.quantity / 100)
    
    def __str__(self):
        return f"{self.food.name} ({self.quantity}g in {self.meal.name})"

