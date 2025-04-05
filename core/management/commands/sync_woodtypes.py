import csv
from django.core.management.base import BaseCommand
from core.models import WoodType

class Command(BaseCommand):
    help = "Microsoft List'ten alınan CSV dosyası ile WoodType verilerini senkronize eder."

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='CSV dosyasının yolu')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {k.strip().lstrip('\ufeff'): v.strip() for k, v in row.items()}
                name = row.get('name')
                if name:
                    WoodType.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('WoodType verileri başarıyla senkronize edildi.'))