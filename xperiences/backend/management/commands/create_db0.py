__author__ = 'ishai'

from django.core.management.base import BaseCommand, NoArgsCommand
from backend.models import *


class Command(NoArgsCommand):

    requires_model_validation = False

    def handle_noargs(self, **options):
        pass
