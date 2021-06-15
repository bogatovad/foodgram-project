from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models.deletion import CASCADE

User = get_user_model()


class Ingredient(models.Model):
    """Model for ingredient."""
    title = models.CharField(max_length=300)
    unit = models.CharField(max_length=200)

    class Meta:
        ordering = ('title',)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.title}, {self.unit}"


class Tag(models.Model):
    """Model for tag."""
    breakfast = 'Завтрак'
    lunch = 'Обед'
    dinner = 'Ужин'

    TAG_CHOICES = [
        (breakfast, 'breakfast'),
        (lunch, 'lunch'),
        (dinner, 'dinner')
    ]

    title = models.CharField(
        verbose_name="Название тега",
        max_length=100,
        unique=True,
        choices=TAG_CHOICES,
    )
    display_name = models.CharField(
        max_length=20,
        verbose_name="Имя тега в шаблоне"
    )
    color = models.CharField(
        max_length=50,
        verbose_name="Цвет тега"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipe(models.Model):
    """Model for recipe."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name='Автор',)
    title = models.CharField(verbose_name="Название рецепта", max_length=200)
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
        blank=True,
        null=True)
    description = models.TextField(
        verbose_name='Текст'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=('recipe', 'ingredient'),
        verbose_name="Ингредиенты"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата публикации"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipe_tags",
        verbose_name="Теги"
    )
    time_to_cook = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.title}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ing"
    )
    amount = models.FloatField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(0),
        ]
    )

    class Meta:
        verbose_name = "Ингредиенты рецепта"
        verbose_name_plural = "Ингредиенты рецептов"

    def __str__(self):
        return f"{self.recipe}, {self.ingredient}, {self.amount}"


class Follow(models.Model):
    """Model for follow."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Тот, на кого подписались")
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'author', ], name='follow_obj'),
    ]

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'Избранный рецепт {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unice_favorite_user_recipe'
            )
        ]
        verbose_name = "Объект избранного"
        verbose_name_plural = "Объекты избранного"


class ShopList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name='Пользователь'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shop_list',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'Покупка репкпта {self.recipe} пользователем {self.user}'

    class Meta:
        verbose_name = "Объект покупки"
        verbose_name_plural = "Объекты покупок"
