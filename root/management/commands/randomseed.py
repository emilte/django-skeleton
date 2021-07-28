# imports
from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth import get_user_model
from start3.nbb import models as nbb_models
from django.contrib.auth import models as auth_models
import random

from django_seed import Seed
# End: imports -----------------------------------------------------------------

# Settings:

User = get_user_model()



class Command(BaseCommand):

    def confirmation(self):
        answer = None
        yes = ['yes', 'y']
        no = ['no', 'n']
        print("== This command will:")
        print("\t 1. Attempt to seed all models")

        print("\n== Are you sure? DOUBLE-CHECK that this is not production server ==")

        while answer not in yes+no:
            answer = input("Type 'y' or 'n': ").lower()

        return answer in yes

    def populate(self):

        seeder = Seed.seeder()

        seeder.add_entity(User, 10)
        seeder.add_entity(nbb_models.Transaction, 300, {
            # 'user': lambda x: users[random.randint(0, users.count()-1 )],
            'cost': lambda x: random.randint(-100, 100),
            'description': lambda x: seeder.faker.sentence(),
        })

        inserted_pks = seeder.execute()


    def handle(self, *args, **options):

        if self.confirmation():
            self.populate()
        else:
            print("== ABORT ==")

        # End of handle
