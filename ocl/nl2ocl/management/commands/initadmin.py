from django.core.management.base import BaseCommand
import django.contrib.auth
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        User = django.contrib.auth.get_user_model()
        user = User.objects.filter(username="som-research").first()
        if user is None:
            user = User.objects.create_user(os.environ.get("ADMIN_USER"), password=os.environ.get("ADMIN_PASSWD"))
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write("SOMOCL user's been created... " + self.style.SUCCESS("OK"))
        else:
            print('SOMOCL users is created only ONCE... ' + self.style.WARNING("NOT CREATED"))