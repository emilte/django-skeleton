# imports
import random
from django_seed import Seed

from django.core import management
from django.contrib.auth import get_user_model; User = get_user_model()
from django.contrib.auth import models as auth_models
from django.core.management.base import BaseCommand

from wiki import models as wiki_models
from events import models as event_models
from gallery import models as gallery_models
from accounts import models as account_models
# End: imports -----------------------------------------------------------------




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

        seeder.add_entity(account_models.Department, 20, {
            'title': lambda x: seeder.faker.word(),
            'parent': lambda x: None,
        })

        seeder.add_entity(User, 30)

        seeder.add_entity(event_models.Event, 20, {
            # 'department': lambda x: seeder.faker.word(),
        })

        seeder.add_entity(gallery_models.Tag, 20, {
            'title': lambda x: seeder.faker.word(),
        })

        seeder.add_entity(gallery_models.Upload, 20, {
            # 'department': lambda x: seeder.faker.word(),
        })

        seeder.add_entity(gallery_models.Quotation, 20, {
            # 'department': lambda x: seeder.faker.word(),
        })

        seeder.add_entity(wiki_models.Folder, 5, {
            'title': lambda x: seeder.faker.word(),
            'root_folder': lambda x: None,
            'perm': lambda x: None,

        })

        seeder.add_entity(wiki_models.Page, 20, {
            'title': lambda x: seeder.faker.word(),
        })

        inserted_pks = seeder.execute()

        groups = auth_models.Group.objects.all()
        for user in User.objects.all():
            random_groups = random.choices( list(groups), k=4)
            user.groups.set(random_groups)

        departments = account_models.Department.objects.all()
        for user in User.objects.all():
            random_departments = random.choices( list(departments), k=4)
            user.departments.set(random_departments)


    def handle(self, *args, **options):

        interactive = options['interactive']
        if interactive:
            if not self.confirmation():
                print("== ABORT ==")
                return
        self.populate()


        # End of handle
