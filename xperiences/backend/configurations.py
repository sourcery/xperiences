from StringIO import StringIO
import simplejson

__author__ = 'ishai'

from configobj import ConfigObj

import settings

config = None

def read_configurations():
    from backend.models import SiteConfiguration
    global config
    conf,_ = SiteConfiguration.objects.get_or_create(name='default')
    print conf
    str = conf.conf or ''
    config = simplejson.loads(str)


read_configurations()

def update_configurations(dict):
    from backend.models import SiteConfiguration
    global config
    for key in dict:
        value = dict[key]
        config[key] = str(value)
    conf,_ = SiteConfiguration.objects.get_or_create(name='default')
    conf.conf = simplejson.dumps(config)
    conf.save()
    read_configurations()

def get_dict():
    global config
    return config

def get_categories():
    global config
    return config.get('CATEGORIES','').split(',')

