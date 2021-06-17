from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient, Tag


def is_tag(request, all_recipes):
    if "tag" in request.GET:
        name_tag = request.GET["tag"]
        return name_tag, all_recipes.filter(tags__title=name_tag)
    return "", all_recipes


def is_tag_favorite(request, favorites):
    if "tag" in request.GET:
        name_tag = request.GET["tag"]
        return name_tag, favorites.filter(recipe__tags__title=name_tag)
    return "", favorites


def get_ingredients(data):
    return [(get_object_or_404(Ingredient, title__exact=data[item]),
             float(data[f"valueIngredient_{item[-1]}"]))
            for item in data if item.startswith("nameIngredient_")]


def get_tags(data):
    return [get_object_or_404(Tag, pk=int(number_key))
            for number_key in dict(data)["tags"]]


def create_response(request, result_ingredients: dict):
    content = "Список ингредиентов для покупок\n\n"

    for ingredient, value in result_ingredients.items():
        content += f"{ingredient[0]}({ingredient[1]}) - {value}\n"

    path_file = f"{request.user}_shop_list"
    response = HttpResponse(content, content_type="text/plain,charset=utf8")
    response["Content-Disposition"] = 'attachment; filename="%s"' % path_file
    return response


def count_total_ingredients(shop_list: list):
    result_ingredients = {}

    for item in shop_list:
        for ingredient in item.recipe.ingredients.all():
            amount = get_object_or_404(
                RecipeIngredient,
                recipe=item.recipe,
                ingredient=ingredient).amount

            if ingredient.title in result_ingredients:
                result_ingredients[(
                    ingredient.title, ingredient.unit)] += amount
            else:
                result_ingredients[(
                    ingredient.title, ingredient.unit)] = amount

    return result_ingredients
