from backend.models import GeoField
import settings

__author__ = 'ishai'

from django.core.management.base import BaseCommand
from django.db.models import get_models
import pymongo

class Command(BaseCommand):


    def handle(self, *args, **options):
        return ensure_geo_fields()

conn = pymongo.Connection()
db = pymongo.database.Database(conn,settings.DATABASES['default']['NAME'])

def ensure_geo_fields(*args, **kwargs):

    models = get_models(kwargs.get('sender',None))
    def ensure_index(collection_name, field_name):
        print collection_name + '.' + field_name
        col = pymongo.collection.Collection(db,collection_name)
        col.ensure_index([(field_name,pymongo.GEO2D)])

    for model in models:
        for field in model._meta.fields:
            if issubclass(GeoField,type(field)):
                ensure_index(model._meta.db_table, str(field.column))
    return 'Done'



