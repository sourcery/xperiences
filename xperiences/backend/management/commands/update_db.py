from experiences.models import Experience

__author__ = 'ishai'

from django.core.management.base import BaseCommand, NoArgsCommand
from backend.models import *


class Command(NoArgsCommand):

    requires_model_validation = False

    def handle_noargs(self, **options):
        exps = Experience.objects.all()
        for exp in exps:
            try:
                if not exp.merchant or not exp.photo1:
                    exp.delete()
                    continue
                for org in exp.originals:
                    exp.originals[org] = None
                exp.save()
            except UserExtension.DoesNotExist:
                exp.delete()
        user_exts = UserExtension.objects.all()

        for user_ext in user_exts:
            try:
                if not user_ext.user:
                    user_ext.delete()
            except User.DoesNotExist:
                user_ext.delete()

        users = User.objects.all()
        for user in users:
            try:
                print user.get_profile()
            except UserExtension.DoesNotExist:
                if not user.is_superuser:
                    user.delete()

