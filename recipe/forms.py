from attr import fields
from django import forms
from .models import Recipe, Ingredient
from django.forms import Select

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title','tags', 'time_to_cook', 'description', 'image')