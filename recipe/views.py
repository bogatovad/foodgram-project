from django.core.paginator import Paginator
from .models import Ingredient, RecipeIngredient, Recipe, ShopList, Tag, User
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ranged_fileresponse import RangedFileResponse
import magic


def index(request):
    all_recipes = Recipe.objects.all()
    name_tag = ''

    if 'tag' in request.GET:
        name_tag = request.GET['tag']
        all_recipes = all_recipes.filter(tags__title=name_tag)

    paginator = Paginator(all_recipes, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    shop_list = ShopList.objects.all()

    if not request.user.is_authenticated:
        return render(request, 'indexNotAuth.html',
                      {'page': page, 'tag': name_tag})
    else:
        return render(request, 'indexAuth.html',
                      {'page': page, 'shop_list': shop_list, 'tag': name_tag})


@login_required
def my_follow(request):
    data = request.user.follower.all()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(request.user)
    return render(request, 'myFollow.html',
                  {'page': page})


def get_ingredients(data):
    return [(Ingredient.objects.get(title__exact=data[item]),
             float(data[f'valueIngredient_{item[-1]}']))
            for item in data if item.startswith('nameIngredient_')]


def get_tags(data):
    return [Tag.objects.get(pk=int(number_key))
            for number_key in dict(data)['tags']]


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ingredients = get_ingredients(request.POST)
        tags = get_tags(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for ingredient in ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient[0],
                    amount=ingredient[1])

            for tag in tags:
                recipe.tags.add(tag)
            return redirect('index')

    return render(request, 'formRecipe.html', {'form': form})


def shop_list(request):
    shop_list = request.user.shop_list.all()
    paginator = Paginator(shop_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'shopList.html', {'page': page})


def favorite(request):
    data = request.user.favorites.all()

    name_tag = ''

    if 'tag' in request.GET:
        name_tag = request.GET['tag']
        data = data.filter(recipe__tags__title=name_tag)

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'favorite.html',
                  {'page': page, 'tag': name_tag})


def add_to_shop_list(request):
    pass


def single_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    if request.user.is_authenticated:
        has_bought_recipe = request.user.shop_list.filter(
            recipe=recipe).exists()
        am_i_follower = request.user.follower.filter(
            author=recipe.author).exists()
        is_it_favorite = request.user.favorites.filter(recipe=recipe).exists()
        return render(request, 'singlePage.html',
                      {'recipe': recipe, 'ingredients': ingredients,
                       'has_bought_recipe': has_bought_recipe,
                       'am_i_follower': am_i_follower,
                       'is_it_favorite': is_it_favorite})
    else:
        return render(request, 'singlePage.html',
                      {'recipe': recipe, 'ingredients': ingredients})


def author_recipe(request, id):
    author = User.objects.get(id=id)
    recipes = author.recipes.all()

    name_tag = ''

    if 'tag' in request.GET:
        name_tag = request.GET['tag']
        recipes = recipes.filter(tags__title=name_tag)

    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        am_i_follower = request.user.follower.filter(author=author).exists()
        return render(request, 'authorRecipe.html',
                      {'author': author, 'page': page,
                       'tag': name_tag,
                       'am_i_follower': am_i_follower})
    else:
        return render(request, 'authorRecipe.html',
                      {'author': author,
                       'page': page, 'tag': name_tag})


def save_shop_list(request):
    shop_list = request.user.shop_list.all()
    result_ingredients = {}

    for item in shop_list:
        for ingredient in item.recipe.ingredients.all():
            amount = RecipeIngredient.objects.get(
                recipe=item.recipe, ingredient=ingredient).amount

            if ingredient.title in result_ingredients:
                result_ingredients[(
                    ingredient.title, ingredient.unit)] += amount
            else:
                result_ingredients[(
                    ingredient.title, ingredient.unit)] = amount

    content = 'Список ингредиентов для покупок\n\n'

    for ingredient, value in result_ingredients.items():
        content += f'{ingredient[0]}({ingredient[1]}) - {value}\n'

    path_file = f'{request.user}_shop_list'
    file = open(path_file, 'w')
    file.write(content)
    file.close()
    response = RangedFileResponse(request, open(
        path_file, 'rb'), content_type=magic.from_file(path_file, mime=True))
    response['Content-Disposition'] = 'attachment; filename="%s"' % path_file
    return response


@login_required
def edit_recipe(request, username: str, id_recipe: int):
    recipe = Recipe.objects.get(author__username=username, id=id_recipe)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)
    if request.method == 'POST':
        ingredients = get_ingredients(request.POST)
        tags = get_tags(request.POST)

        if form.is_valid():
            recipe.save()

            for ingredient in ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient[0],
                    amount=ingredient[1])

            for tag in recipe.tags.all():
                recipe.tags.remove(tag)

            for tag in tags:
                recipe.tags.add(tag)

            return redirect('index')
    return render(request, 'formRecipe.html',
                  {'form': form, 'edit': True, 'id_recipe': id_recipe})


def delete_recipe(request, id_recipe):
    Recipe.objects.filter(id=id_recipe).delete()
    return redirect('index')
