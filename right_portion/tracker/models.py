from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField(help_text="per_100_grams")
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return self.name


# class Meal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     food = models.ForeignKey(Food, on_delete=models.CASCADE)
#     quantity = models.FloatField(help_text="grams")
#     date = models.DateField(auto_now_add=True)

#     def total_calories(self):
#         return (self.food.calories * self.quantity) / 100
