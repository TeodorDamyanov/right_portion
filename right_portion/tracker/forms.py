from django import forms
from .models import Meal, MealFood, Food

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories', 'protein', 'carbs', 'fats']

class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = ['food', 'quantity']

MealFoodFormSet = forms.inlineformset_factory(
    Meal,
    MealFood,
    form=MealFoodForm,
    extra=1,
    can_delete=True
)
