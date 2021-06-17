from django.urls import path

from .views import (author_recipe, create_recipe, delete_recipe, edit_recipe,
                    favorite, index, my_follow, save_shop_list, shop_list,
                    single_recipe)

urlpatterns = [
    path("", index, name="index"),
    path("my_follow/", my_follow, name="my_follow"),
    path("create_recipe/", create_recipe, name="create_recipe"),
    path("favorite/", favorite, name="favorite"),
    path("shop_list/", shop_list, name="shop_list"),
    path("single_recipe/<int:id>/", single_recipe, name="single_recipe"),
    path("author_recipe/<int:id>/", author_recipe, name="author_recipe"),
    path("save_shop_list/", save_shop_list, name="save_shop_list"),
    path("edit_recipe/<str:username>/<int:id_recipe>/",
         edit_recipe, name="edit_recipe"),
    path("delete_recipe/<int:id_recipe>/",
         delete_recipe, name="delete_recipe"),
]
