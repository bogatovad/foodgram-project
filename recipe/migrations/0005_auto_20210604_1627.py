# Generated by Django 2.2.6 on 2021-06-04 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
    ]
