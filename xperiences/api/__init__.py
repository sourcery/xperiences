import datetime
from django.template.context import Context
from django.utils import simplejson
import time
from django.db.models.fields.files import FileField, FieldFile
from django.template import loader
from backend.models import XPImageField
from piston.decorator import decorator
from piston.emitters import Emitter
from piston.utils import Mimer, rc

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
    if isinstance(thing.field, XPImageField):
        c = Context({'photo' : thing })
        html_template = loader.get_template('photo.json')
        if html_template == None:
            return None
        content = html_template.render(c)
        print content
        return simplejson.loads(content)
    return { 'url' : thing.url }

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

def user_enitity_permission(model=None,field_name='user_id'):

    @decorator
    def wrap(f, self, request,id=None,*args, **kwargs):
    #        if field_name not in request.POST or request.POST[field_name] == '':
    #            return rc.BAD_REQUEST
    #        user_id = int(request.POST[field_name])
        _model = (model or self.model)
        if not id:
            id = request.POST.get(_model._meta.pk.name) or request.GET.get(_model._meta.pk.name)
        if not id:
            return rc.FORBIDDEN
        user_id = request.session['_auth_user_id']
        obj = _model.objects.get(id=id)
        field_name_parts = field_name.split('.')
        attr = None
        for field_name_part in field_name_parts:
            parent = attr or obj
            attr = getattr(parent,field_name_part)
            if not attr:
                break
        if attr != user_id:
            return rc.FORBIDDEN
        kwargs['obj'] = obj
        return f(self,request,*args,**kwargs)
    return wrap

def flag_user_logged_in(user_id):
    pass

def allow_only_authenticated():
    @decorator
    def wrap(f, self, request, *args, **kwargs):
        if request.user.is_anonymous() and request.user_extension:
            resp = rc.FORBIDDEN
            resp.write("User is not authenticated")
            return resp
        flag_user_logged_in(request.session['_auth_user_id'])
        return f(self,request,*args,**kwargs)
    return wrap
