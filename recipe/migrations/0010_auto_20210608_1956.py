# Generated by Django 2.2.6 on 2021-06-08 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_auto_20210607_2124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='count',
            new_name='amount',
        ),
    ]
