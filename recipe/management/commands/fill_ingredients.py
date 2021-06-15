from django.core.management.base import BaseCommand
import csv
import os

from grocery_assistant.settings import BASE_DIR
from recipe.models import Ingredient

CSV_FILE = os.path.join(BASE_DIR, "ingredients/ingredients.csv")


class Command(BaseCommand):
    help = "Collect csv to db"

    def handle(self, *args, **options):
        with open(CSV_FILE, encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                title, unit = row
                Ingredient.objects.get_or_create(title=title, unit=unit)
