# imports
from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth import get_user_model
from start3.nbb import models as nbb_models
from start3.barvakt import models as barvakt_models
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
        devs = User.objects.all()

        seeder = Seed.seeder()
        seeder.faker.seed_instance(1234)

        seeder.add_entity(auth_models.Group, 20, {
            'name': lambda x: seeder.faker.word(),
        })
        seeder.add_entity(User, 30)
        seeder.add_entity(nbb_models.Transaction, 300, {
            # 'user': lambda x: users[random.randint(0, users.count()-1 )],
            'cost': lambda x: random.randint(-100, 100),
            'description': lambda x: seeder.faker.sentence(),
        })
        seeder.add_entity(nbb_models.BarList, 4)
        seeder.add_entity(nbb_models.Item, 10, {
            'name': lambda x: seeder.faker.word(),
            'description': lambda x: seeder.faker.sentence(),
            'cost': lambda x: random.randint(5, 100),
        })

        inserted_pks = seeder.execute()

        groups = auth_models.Group.objects.all()
        for user in User.objects.all():
            random_groups = random.choices( list(groups), k=4)
            user.groups.set(random_groups)


    def handle(self, *args, **options):

        if self.confirmation():
            self.populate()
        else:
            print("== ABORT ==")

        # End of handle
