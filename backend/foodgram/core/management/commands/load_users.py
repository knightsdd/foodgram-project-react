import csv

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Load a users csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            next(reader, None)
            for row in reader:
                user = User.objects.create(
                    username=row[1],
                    email=row[2],
                    first_name=row[3],
                    last_name=row[4],
                )
                user.set_password(row[5])
                user.save()
