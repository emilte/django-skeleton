# imports
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core import management
from django.contrib.auth import get_user_model
import getpass
# End: imports -----------------------------------------------------------------

# Settings:

User = get_user_model()

EMAILS = [
    'emil.telstad@gmail.com',
]

DEVS = [
    ('emilte'),
]

U = [
    {
        'username': 'emilte',
        'email': 'emil.telstad@gmail.com',
        'first_name': 'Emil',
        'last_name': 'Telstad',
        'phone_number': 12345678,
        'sex': User.MALE,
    }
]

PASSWORD = "Django123"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def confirmation(self):
        answer = None
        yes = ['yes', 'y']
        no = ['no', 'n']
        print("== This command will:")
        print("\t 1. Set following users as superuser:")
        for u in U:
            print(f"\t\t {u['username']}")

        print("\n== Are you sure? DOUBLE-CHECK that this is not production server ==")

        while answer not in yes+no:
            answer = input("Type (Y)es or (N)o: ").lower()

        return answer in yes

    def f(self):
        # Set super devs for NICKNAMES:
        for u in U:
            user, created = User.objects.get_or_create(username=u['username'])
            user.is_staff = True
            user.is_superuser = True
            user.set_password(PASSWORD)
            try:
                user.email = u['email']
                user.first_name = u['first_name']
                user.last_name = u['last_name']
                user.phone_number = u['phone_number']
                user.sex = u['sex']
            except Exception as e:
                print("Non-required fields failed")
                print(e)

            user.save()
        # End: f


    def handle(self, *args, **options):
        print("\n== COMMAND: sudev ==")
        if options['interactive']:
            if self.confirmation():
                self.f()
            else:
                print("== ABORT ==")
        self.f()

        # End of handle
