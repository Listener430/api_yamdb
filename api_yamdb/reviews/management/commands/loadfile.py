from django.core.management.base import BaseCommand
from django.apps import apps
import csv


class Command(BaseCommand):
    help = "Creating model objects according the file path specified"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="file path")
        parser.add_argument("--model_name", type=str, help="model name")

    def handle(self, *args, **options):
        file_path = options["path"]
        _model = apps.get_model("reviews", options["model_name"])
        try:
            with open(file_path, "r", encoding="utf8") as csv_file:
                reader = csv.reader(csv_file, delimiter=",", quotechar="|")
                header = next(reader)
                for row in reader:
                    _object_dict = {
                        key: value for key, value in zip(header, row)
                    }
                    _model.objects.create(**_object_dict)
                print("загрузилось")
        except Exception:
            print("что-то неполучилось")
