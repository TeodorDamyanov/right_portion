from django.db import models
from django.contrib.auth.models import User
from right_portion import settings

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField(help_text="per_100_grams")
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.calories} cals"
    

class Plan(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    num_days = models.IntegerField()
    daily_calories = models.FloatField()
    protein_goal = models.FloatField()
    carbs_goal = models.FloatField()
    fats_goal = models.FloatField()

    def __str__(self):
        return f"{self.user.username}'s Plan - {self.daily_calories} kcal/day"


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

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
        return self.food.calories * self.quantity / 100
    
    @property
    def total_protein(self):
        return self.food.protein * self.quantity / 100

    @property
    def total_carbs(self):
        return self.food.carbs * self.quantity / 100

    @property
    def total_fats(self):
        return self.food.fats * self.quantity / 100
    
    def __str__(self):
        return f"{self.food.name} ({self.quantity}g in {self.meal.name})"

