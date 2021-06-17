from django.contrib import admin
from django.contrib.admin import register

from . import models
from .models import Favorite, Follow, ShopList, Tag


@register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "unit",
    )
    search_fields = (
        "title",
    )
    list_filters = (
        "unit",
    )


@register(models.RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = (
        "ingredient",
        "recipe",
        "count"
    )
    search_fields = (
        "ingredient",
        "recipe",
    )


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    min_num = 1
    extra = 0


@register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "pub_date",
    )
    search_fields = (
        "name",
    )
    list_filter = (
        "author",
    )
    autocomplete_fields = (
        "ingredients",
    )
    inlines = (
        RecipeIngredientInline,
    )


admin.site.register(Tag)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShopList)
