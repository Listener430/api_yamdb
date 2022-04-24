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
        with open(file_path, "r", encoding="utf8") as csv_file:
            reader = csv.reader(csv_file, delimiter=";", quotechar="|")
            header = next(reader)
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                opts = _model._meta
                print(_object_dict)
                print(opts)
                other_fields = [
                    field for field in opts.get_fields() if field.many_to_one
                ]
                print("внешние ключи", other_fields)
                id = _object_dict.get("id")
                try:
                    obj = _model.objects.get(pk=id)
                    print("запись уже существует", obj)
                    continue
                except _model.DoesNotExist:
                    try:
                        if other_fields:
                            for field in other_fields:
                                print(field.name)
                                rel_model = opts.get_field(
                                    field.name
                                ).related_model
                                print(rel_model)
                                try:
                                    print(field)
                                    print("test")
                                    print(_object_dict.get(field.name))
                                    rel_obj = rel_model.objects.get(
                                        id=_object_dict.get(field.name)
                                    )
                                    print("test")
                                except rel_model.DoesNotExist:
                                    rel_obj = rel_model.objects.create(
                                        id=_object_dict.get(field.name)
                                    )

                                _object_dict.update({field.name: rel_obj})
                                print(_object_dict)
                    except _model.DoesNotExist:
                        pass
                    print(_object_dict)
                    obj = _model.objects.create(**_object_dict)
                    print("создали запись")
                except _model.MultipleObjectsReturned:
                    print("неуникальный ключx`", id)
                    pass
