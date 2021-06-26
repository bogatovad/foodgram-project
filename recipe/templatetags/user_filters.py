from django import template

from ..models import Follow

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def in_list(recipe, show_list):
    return show_list.filter(recipe=recipe).exists()


@register.filter
def in_favorites_list(recipe_favorites, user):
    return recipe_favorites.filter(user=user).exists()


@register.filter()
def is_following(author, user):
    return Follow.objects.filter(user=user, author=author).exists()
