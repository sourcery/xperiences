from django.utils import simplejson


def read_configurations():
    from backend.models import SiteConfiguration
    conf, _ = SiteConfiguration.objects.get_or_create(name='default')
    print conf
    str = conf.conf or '{}'
    try:
        return simplejson.loads(str)
    except Exception:
        return {}
config = read_configurations()


def update_configurations(dict):
    from backend.models import SiteConfiguration
    global config, categories
    for key in dict:
        value = dict[key]
        config[key] = str(value)
    conf, _ = SiteConfiguration.objects.get_or_create(name='default')
    conf.conf = simplejson.dumps(config)
    conf.save()
    categories = None
    config = read_configurations()

categories = None
def get_categories():
    global config, categories
    if not categories:
        categories = config.get('CATEGORIES','cat1,cat2').split(',')
    return categories

def get_categories_as_choices():
    cats = get_categories()
    return [(cat,cat) for cat in cats]

