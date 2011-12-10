from experiences.models import Experience

__author__ = 'ishai'

from django.core.management.base import BaseCommand, NoArgsCommand
from backend.models import *


class Command(NoArgsCommand):

    requires_model_validation = False

    def handle_noargs(self, **options):
        exps = Experience.objects.all()
        for exp in exps:
            for org in exp.originals:
                exp.originals[org] = None
            exp.save()

