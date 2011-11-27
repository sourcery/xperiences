__author__ = 'ishai'

from configobj import ConfigObj

import settings

config = None

def read_configurations():
    global config

    config = ConfigObj(settings.SITE_CONFIGURATION_FILE)


read_configurations()

def update_configurations(dict):
    global config
    for key in dict:
        value = dict[key]
        config[key] = str(value)
    config.write()
    read_configurations()

def get_dict():
    global config
    return config

def get_categories():
    global config
    return config.get('CATEGORIES','').split(',')

