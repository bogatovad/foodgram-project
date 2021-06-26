from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, RecipeIngredient
from .utils import get_ingredients, get_tags


def create_ingredients(ingredients, recipe):
    for ingredient in ingredients:
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient[0],
            amount=ingredient[1])


def create_tags(tags, recipe):
    for tag in recipe.tags.all():
        recipe.tags.remove(tag)
    for tag in tags:
        recipe.tags.add(tag)


class RecipeForm(forms.ModelForm):
    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        ingredients = get_ingredients(self.data)
        tags = get_tags(self.data)
        recipe.save()
        create_ingredients(ingredients, recipe)
        create_tags(tags, recipe)
        return recipe

    class Meta:
        model = Recipe
        fields = ("title", "tags", "time_to_cook", "description", "image")

    def clean(self):
        ingredients = get_ingredients(self.data)
        amount = ingredients[0][1]
        if amount < 0:
            raise ValidationError(
                "Количетсво ингредиента не может быть отрицательным")
        return self.cleaned_data
