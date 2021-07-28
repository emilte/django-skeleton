# imports
import os
import glob

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def handle(self, *args, **options):
        for app in settings.PROJECT_APPS:
            
            try:
                path = app.replace('.', '/')
                migrations = f"{path}/migrations"
                os.mkdir(migrations)
                init = f"{migrations}/__init__.py"
                open(init, 'a').close()
                
            except Exception as e:
                pass
                # print(f"{app} failed. {e}")
