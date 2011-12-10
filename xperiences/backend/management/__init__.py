from commands.ensure_geo_fields import  ensure_geo_fields, ensure_text_fields

__author__ = 'ishai'
from django.db.models import signals

signals.post_syncdb.connect(ensure_geo_fields, dispatch_uid = "backend.ensure_geo_fields")

signals.post_syncdb.connect(ensure_text_fields, dispatch_uid = "backend.ensure_text_fields")

  