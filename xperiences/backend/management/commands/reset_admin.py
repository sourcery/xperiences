from django.contrib.auth.models import User

__author__ = 'ishai'

from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        user.set_password('admin')
        user.is_active = True
        user.save()
        return 'Done'

