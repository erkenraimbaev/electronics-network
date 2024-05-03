
import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='super_admin@mail.ru',
            first_name='Admin',
            last_name='Adminov',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('PASSWORD_SUPER_USER'))
        user.save()
