from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone="+79242424242",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            invite_code='4ZJLJj'
        )
        user.set_password('1234qwer')
        user.save()
