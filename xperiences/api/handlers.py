from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from backend.models import UserExtension, UserMessage
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
from pymongo.objectid import ObjectId
import re


Emitter.register('json', api.EmpeericJSONEmitter, 'application/json; charset=utf-8')
MAX_RESULTS_PER_QUERY = 100
# Base class for handler
class MyBaseHandler(BaseHandler):
    allowed_methods = ()
    # BMU extensions:
    # defines which fields are opened for update, currently not affects create
    update_fields = ()
    # maps a handler for a model, defines the data emition for related objects by foreign-keys
    mappings = {}

    def read(self,request,*args,**kwargs):
        limit = int(kwargs.get('limit',50))
        if 'limit' in kwargs:
            del kwargs['limit']
        if limit > MAX_RESULTS_PER_QUERY:
            limit = MAX_RESULTS_PER_QUERY
        offset = int(kwargs.get('offset',0))
        if 'offset' in kwargs:
            del kwargs['offset']
        return super(MyBaseHandler,self).read(request,*args,**kwargs)[offset:limit]


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
                        elif type(field) == models.IntegerField or type(field) == models.BigIntegerField:
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
    query_fields = ('is_active','keywords','lat','lng','category','max_distance','merchant','of_merchant')

    def read(self,request,*args,**kwargs):
        params = dict([ (k,request.GET[k].strip()) for k in request.GET])
        params['limit'] = params.get('limit',10)

        filter_params = {}
        for key in params:
            if (key in self.query_fields or key in ('limit','offset')) and params[key] and params[key] != '':
                filter_params[key] = params[key]
        params = filter_params

        of_merchant = 'of_merchant' in params and request.merchant
        if of_merchant:
            params['merchant'] = request.merchant
            del params['of_merchant']
            return super(ExperienceHandler,self).read(request,*args,**params)
        else:
            params['is_active'] = True


        lat = params.get('lat')
        lng = params.get('lng')
        if lat:
            del params['lat']
            lat = float(lat)
        if lng:
            del params['lng']
            lng = float(lng)



        limit = int(params.get('limit',10))
        if 'limit' in params:
            del params['limit']
        if limit > MAX_RESULTS_PER_QUERY:
            limit = MAX_RESULTS_PER_QUERY
        offset = int(params.get('offset',0))
        if 'offset' in params:
            del params['offset']

        if 'category' in params:
            categories = params.pop('category').split(',')
#            if len(categories) > 0 and categories[0] != '':
            category_objects = [ObjectId(c) for c in categories]
            params['category_id'] = { '$in' : category_objects}
        if 'keywords' in params:
            keywords = params.pop('keywords').split(' ')
            keywords_regex ='.*' + ('.*'.join([k.strip() for k in keywords])) + '.*'
            params["$or"] = [{'description': { '$regex' : keywords_regex }},{'title': { '$regex' : keywords_regex }}]

        more_args = {}
        if 'max_distance' in params:
            more_args['max_distance'] = params.pop('max_distance')

        if lat and lng:
            return Experience.objects.proximity_query( { 'lat' : float(lat), 'lng' : float(lng)},query=params,**more_args)[offset:limit]
        else:
            return Experience.objects.raw_query(params)[offset:limit]

    @api.user_enitity_permission(field_name='merchant.user_id', id_field_name='slug_id')
    def update(self,request,*args,**kwargs):
        return super(ExperienceHandler,self).update(request, **kwargs)

class MessageHandler(MyBaseHandler):
    allowed_methods = ('DELETE','POST')
    model = UserMessage

    @api.user_enitity_permission(field_name='to.user_id')
    def delete(self, request,id=None, obj=None, *args, **kwargs):
        return obj.delete()

    @api.allow_only_authenticated()
    def create(self,request,*args,**kwargs):
        params = dict([ (k,request.POST[k].strip()) for k in request.POST])
        to__id = params.pop('to__id')
        to = UserExtension.objects.get(id=to__id)
        return super(MessageHandler,self).create(request,{'sender':request.user_extension,'to':to},**params)

