# imports
import os
import glob
import shutil

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

# End: imports -----------------------------------------------------------------


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ Delete all migration files for each installed app """

        for app in settings.INSTALLED_APPS:
            try:
                path = app.replace('.', '/')
                migrations = f"{path}/migrations"
                app_migrations = glob.glob(f"{migrations}/[0-9]*")

                for f in app_migrations:
                    os.remove(f)
                    print(f"Removed {f}")
                    
                pycache = f"{migrations}/__pycache__"
                shutil.rmtree(pycache)
                print(f"Removed {pycache}")

            except Exception as e:
                pass
                # print(f"{app} failed. {e}")
