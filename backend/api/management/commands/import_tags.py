import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Tag


class Command(BaseCommand):
    help = "Импорт тегов из файла"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "data", "tags.csv")
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                name, slug = row
                Tag.objects.get_or_create(name=name, slug=slug)
        self.stdout.write(self.style.SUCCESS("Теги успешно импортированы"))
