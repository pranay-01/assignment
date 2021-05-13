from django.core.management.base import BaseCommand
from vehicles.models import Manufacturer


class Command(BaseCommand):
    help = 'simple command demo'

    def add_arguments(self, parser):

        parser.add_argument('number', nargs='+', type= int, help= 'give some number(s)')

        parser.add_argument('--mesg', type=str, help = 'enter a message')

    def handle(self, *args, **options):

        ids = options['number']
        mesg = options['show']

        for each in ids:
            if Manufacturer.objects.filter(pk=each).exists():
                print('Yep,its there')
                print('here is a message' + mesg)
            else:
                print('Sorry')