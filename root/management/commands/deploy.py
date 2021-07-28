# imports
import os
import glob

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def handle(self, *args, **options):
        management.call_command('deploymigrations')
        management.call_command('flush')
        management.call_command('sudev')
        management.call_command('collectstatic', interactive=False)
