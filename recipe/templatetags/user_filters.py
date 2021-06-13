from django import template

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