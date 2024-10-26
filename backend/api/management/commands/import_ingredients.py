import csv
import os

from api.models import Ingredient
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Импорт ингредиентов из файла"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "data", "ingredients.csv")
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, unit = row
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
        self.stdout.write(self.style.SUCCESS(
            "Ингредиенты успешно импортированы"))
