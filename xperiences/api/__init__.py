import datetime
from django.template.context import Context
from django.utils import simplejson
import time
from django.db.models.fields.files import FileField, FieldFile
from django.template import loader
from piston.emitters import Emitter
from piston.utils import Mimer

__author__ = 'ishai'

class EmpeericJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            d = time.mktime(o.utctimetuple())
            return r"/Date(%u000)/" % d
        else:
            return super(EmpeericJSONEncoder, self).default(o)

Mimer.register(lambda *a: None, ('application/x-www-form-urlencoded; charset=UTF-8',))

def parse_file_field(thing):
    if not thing:
        return None
    c = Context({'photo' : thing })
    html_template = loader.get_template('photo.json')
    if html_template == None:
        return None
    content = html_template.render(c)
    print content
    return simplejson.loads(content)

class EmpeericJSONEmitter(Emitter):
    """
    JSON emitter, understands timestamps.
    """

    special_types = { FieldFile : parse_file_field }

    def render(self, request):
        cb = None
        if request:
            cb = request.GET.get('callback')
        obj = self.construct()


        seria = simplejson.dumps(obj, cls=EmpeericJSONEncoder, ensure_ascii=True, indent=None, separators=(',', ':'))

        # Callback
        if cb:
            return '%s(%s)' % (cb, seria)

        return seria



    def decode_datetime(self, dt):
        return dict({
            'datetime' : self.decode_full_datetime(dt),
            'ago' : self.decode_time_interval(datetime.datetime.now() - dt),
            'date' : self.decode_date(dt),
            'time' : self.decode_time(dt)
        })

    def decode_date(self, dt):
        return str(dt.date())

    def decode_time(self, dt):
        return dt.strftime('%H:%M')

    def decode_full_datetime(self, dt):
        return str(dt)

    def decode_time_interval(self, ti):
        if ti.days >= 30:
            return '%d monthes' %(ti.days/30)
        if ti.days >= 7:
            return '%d weeks' % (ti.days/7)
        if ti.days >= 1:
            return '%d days' % ti.days
        if ti.seconds >= 3600:
            return '%d hours' % (ti.seconds/3600)
        if ti.seconds >= 60:
            return '%d minutes' % (ti.seconds/60)
        return '%d seconds' % (ti.seconds)
  