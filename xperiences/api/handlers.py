from django.contrib.auth.models import User
from django.db import models
from backend.models import UserExtension
from experiences.models import Experience

__author__ = 'ishai'

from datetime import timedelta, datetime
import threading
from piston.emitters import Emitter, JSONEmitter
from django.db.models.base import Model
from piston.resource import UploadRequestHandler
from piston.utils import rc, throttle
import logging
from piston.handler import BaseHandler
from backend import models as my_models
import api

Emitter.register('json', api.EmpeericJSONEmitter, 'application/json; charset=utf-8')

# Base class for handler
class MyBaseHandler(BaseHandler):
    allowed_methods = ()
    # BMU extensions:
    # defines which fields are opened for update, currently not affects create
    update_fields = ()
    # maps a handler for a model, defines the data emition for related objects by foreign-keys
    mappings = {}

    def update(self, request, additions=None,update_fields=None,*args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED
        update_fields = update_fields or self.update_fields

        attrs = self.flatten_dict(request.POST)
        if additions:
            attrs.update(additions)
        pkfield = self.model._meta.pk.name

        id = attrs.get(pkfield)

        fields_by_name = dict((f.name,f) for f in self.model._meta.fields)

        try:
            if 'obj' in kwargs:
                inst = kwargs['obj']
            else:
                if id:
                    inst = self.model.objects.get(pk=id)
                else:
                    inst = self.model.objects.get(**attrs)
            for k,v in attrs.items():
                if (len(update_fields) == 0 or k in update_fields):
                    try:
                        key = k.split('_id')[0]
                        field = fields_by_name[key]
                        if field:
                            try:
                                if type(field) == models.CharField:
                                    value = v
                                elif type(field) == models.BooleanField:
                                    value = v == True or v == 'true'
                                elif type(field) == models.IntegerField or type(field) == models.BigIntegerField or type(field) == models.ForeignKey:
                                    value = int(v)
                                elif type(field) == models.FloatField:
                                    value = float(v)
                                elif type(field) == models.DateTimeField or type(field) == models.TimeField or type(field) == models.DateField:
                                    value = datetime.strptime(v,'%Y-%m-%d-%H-%M')
                                else:
                                    value = v
                            except:
                                value = v
                            setattr(inst,k,value)
                    except:
                        pass
            inst.save()
            return inst
        except self.model.DoesNotExist:
            return rc.NOT_FOUND
        except self.model.MultipleObjectsReturned:
            return rc.DUPLICATE_ENTRY

    def create(self, request, additions, *args, **kwargs):
        if not self.has_model():
            return rc.NOT_IMPLEMENTED

        attrs = self.flatten_dict(request.POST)
        attrs.update(additions)
        fields_by_name = dict((f.name,f) for f in self.model._meta.fields)
        for k,v in attrs.items():
            key = k.split('_id')[0]
            if not key in fields_by_name:
                del attrs[k]
            else:
                field = fields_by_name[key]
                if self.model._meta.pk == field:
                    del attrs[k]
                else:
                    try:

                        if type(field) == models.CharField:
                            value = v
                        elif type(field) == models.BooleanField:
                            value = v == True or v == 'true'
                        elif type(field) == models.IntegerField or type(field) == models.BigIntegerField or type(field) == models.ForeignKey:
                            value = int(v)
                        elif type(field) == models.FloatField:
                            value = float(v)
                        elif type(field) == models.DateTimeField or type(field) == models.TimeField or type(field) == models.DateField:
                            value = datetime.strptime(v,'%Y-%m-%d-%H-%M')
                        else:
                            value = v
                    except:
                        value = v
                    attrs[k] = value

        inst = self.model(**attrs)
        inst.save()
        return inst

    # Another way of defining a handler for object attributes emission is in get_mapping which lets you decide on a different handler each time
    # if not overriden will use self.mappings
    def get_mapping(self, data,root_data,user_id):
        model = type(data)
        if model in self.mappings:
            return self.mappings[model]
        else:
            return None

class UserHandler(MyBaseHandler):
    model = User
    fields = ('id','first_name','last_name','full_name','short_name','email')

class MerchantHandler(MyBaseHandler):

    model = UserExtension
    fields = ('id','name', 'description','user','photo')

class ExperienceHandler(MyBaseHandler):
    allowed_methods = ('GET','PUT',)
    model = Experience
    fields = ('slug_id', 'title','description','merchant','photo1','photo2','photo3','photo4','photo5','price','capacity','valid_from','valid_until','is_active')
    update_fields = ('is_active',)

    def read(self,request,*args,**kwargs):
        params = dict([ (k,request.GET[k]) for k in request.GET])
        of_merchant = 'of_merchant' in params and request.merchant
        if of_merchant:
            params['merchant'] = request.merchant
            del params['of_merchant']
        else:
            params['is_active'] = True
        lat = params.get('lat')
        lng = params.get('lng')
        if lat:
            del params['lat']
        if lng:
            del params['lng']

        if 'id' in params or not lat  or not lng:
            return super(ExperienceHandler,self).read(request,*args,**params)
        else:
            return Experience.objects.proximity_query( { 'lat' : float(lat), 'lng' : float(lng)}, query=params)

    def update(self,request,*args,**kwargs):
        return super(ExperienceHandler,self).update(request)
