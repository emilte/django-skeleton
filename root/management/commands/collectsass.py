# imports
from django.core import management
from django.conf import settings
from django.core.management.base import BaseCommand

# End: imports -----------------------------------------------------------------


class Command(BaseCommand):
    """
    Useful command incase you are using the django-sass package
    
    This lets you use lets you use collectsass, similarly to collectstatic.
    Separate project apps with sass development into PROJECT_APPS in settings 
    """

    def handle(self, *args, **options):
        for app in settings.PROJECT_APPS:
            try:
                path = app.split(".")
                input = f"{'/'.join(path)}/static/{path[-1]}/scss/"
                output = f"{'/'.join(path)}/static/{path[-1]}/css/"
                # print(f"sass {input} {output}")
                print(app)
                management.call_command("sass", input, output)
            except:
                print("failed")

        management.call_command("collectstatic", interactive=False)
