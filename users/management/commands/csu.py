from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = User.objects.create(email="admin@example.com")
        email.set_password("123qwe")
        email.is_active = True
        email.is_staff = True
        email.is_superuser = True
        email.save()
