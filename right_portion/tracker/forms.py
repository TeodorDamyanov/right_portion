from django import forms
from .models import Meal, MealFood, Food

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name']

class MealFoodForm(forms.ModelForm):
    class Meta:
        model = MealFood
        fields = ['food', 'quantity']

MealFoodFormSet = forms.inlineformset_factory(
    Meal,                # parent model
    MealFood,            # child model
    form=MealFoodForm,
    extra=1,             # how many food fields to show by default
    can_delete=True
)
