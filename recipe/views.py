from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe, RecipeIngredient, ShopList, User
from .utils import (count_total_ingredients, create_response,
                    is_tag, is_tag_favorite)


def get_paginator(request, data: QuerySet):
    """Return a paginator.
    Keyword arguments:
    request -- HttpRequest's object
    data    -- Data that we need to split on pages
    """
    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    """Return the main page."""
    all_recipes = Recipe.objects.all()
    name_tag, all_recipes = is_tag(request, all_recipes)
    page = get_paginator(request, all_recipes)
    shop_list = ShopList.objects.all()
    context = {"page": page, "tag": name_tag}

    if request.user.is_authenticated:
        context.update({"shop_list": shop_list})

    return render(request, "index.html", context)


@login_required
def my_follow(request):
    """Return user's followers."""
    data = request.user.follower.all()
    page = get_paginator(request, data)
    return render(request, "myFollow.html", {"page": page})


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect("index")

    return render(request, "formRecipe.html", {"form": form})


@login_required
def edit_recipe(request, username: str, id_recipe: int):
    """Edit user's recipe.
    Keyword arguments:
    username  -- Author's username of recipe.
    id_recipe -- recipe's id which author is editing.
    """
    recipe = Recipe.objects.get(author__username=username, id=id_recipe)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe)

    if form.is_valid():
        form.save()
        return redirect("index")

    return render(
        request,
        "formRecipe.html",
        {"form": form, "edit": True, "id_recipe": id_recipe})


def shop_list(request):
    """Return users's shop list."""
    shop_list = request.user.shop_list.all()
    page = get_paginator(request, shop_list)
    return render(request, "shopList.html", {"page": page})


def favorite(request):
    """Return users's favorite recipes."""
    favorites = request.user.favorites.all()
    name_tag, favorites = is_tag_favorite(request, favorites)
    page = get_paginator(request, favorites)
    return render(request, "favorite.html",
                  {"page": page, "tag": name_tag})


def single_recipe(request, id: int):
    """Return singe page's recipe."""
    recipe = Recipe.objects.get(id=id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    context = {"recipe": recipe, "ingredients": ingredients}

    if request.user.is_authenticated:
        has_bought_recipe = request.user.shop_list.filter(
            recipe=recipe).exists()
        am_i_follower = request.user.follower.filter(
            author=recipe.author).exists()
        is_it_favorite = request.user.favorites.filter(recipe=recipe).exists()

        context.update({"has_bought_recipe": has_bought_recipe,
                        "am_i_follower": am_i_follower,
                        "is_it_favorite": is_it_favorite})

    return render(request, "singlePage.html", context)


def author_recipe(request, id: int):
    """Return author's page of recipes.
    Keyword arguments:
    id -- Author's id.
    """
    author = get_object_or_404(User, id=id)
    all_recipes = author.recipes.all()
    name_tag, all_recipes = is_tag(request, all_recipes)
    page = get_paginator(request, all_recipes)
    context = {"author": author, "page": page, "tag": name_tag}

    if request.user.is_authenticated:
        am_i_follower = request.user.follower.filter(author=author).exists()
        context.update({"am_i_follower": am_i_follower})

    return render(request, "authorRecipe.html", context)


def save_shop_list(request):
    """Download users's shop list as txt file."""
    shop_list = request.user.shop_list.all()
    result_ingredients = count_total_ingredients(shop_list)
    return create_response(request, result_ingredients)


def delete_recipe(request, id_recipe: int):
    Recipe.objects.filter(id=id_recipe).delete()
    return redirect("index")


def page_not_found(request, exception):
    return render(
        request,
        "404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "500.html", status=500)
