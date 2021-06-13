# Generated by Django 2.2.6 on 2021-06-04 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20210604_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(choices=[('Завтрак', 'breakfast'), ('Обед', 'lunch'), ('Ужин', 'dinner')], max_length=100, unique=True, verbose_name='Название тега'),
        ),
    ]
