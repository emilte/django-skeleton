# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from accounts.models import *
# End: imports -----------------------------------------------------------------

# Settings:
USER_PW = "Django123"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def createsu(self):
        username = "admin"
        email = "admin@admin.com"
        User.objects.create_superuser(
            username=username,
            email=email,
            password=USER_PW,
            first_name="Admin",
            last_name="Adminsen",
            phone_number=12345678,
            sex=User.OTHER,
        )


    def handle(self, *args, **options):
        try:
            self.createsu()
        except Exception as e:
            print(e)
        # End of handle
