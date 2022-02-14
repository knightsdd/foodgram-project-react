import csv

from django.core.management import BaseCommand
from tags.models import Tag


class Command(BaseCommand):
    help = 'Load a tags csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            next(reader, None)  # skip the header
            for row in reader:
                Tag.objects.create(
                    name=row[1],
                    color=row[2],
                    slug=row[3],
                )
