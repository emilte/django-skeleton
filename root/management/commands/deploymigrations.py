# imports
import os
import glob

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def handle(self, *args, **options):
        management.call_command('migratezero')
        management.call_command('deletemigrations')
        management.call_command('setupmigrations2')
        management.call_command('makemigrations')
        management.call_command('migrate')
