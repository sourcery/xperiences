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
        config[key] = value
    conf, _ = SiteConfiguration.objects.get_or_create(name='default')
    conf.conf = simplejson.dumps(config)
    conf.save()
    categories = None
    config = read_configurations()

categories = None
def get_categories():
    global config, categories
    if not categories:
        categories = config.get('CATEGORIES',[('Hosted Meal','Hosted Meal') ,('Personal Chef','Personal Chef'), ('DIY Food Class','DIY Food Class'), ('Food Artisan', 'Food Artisan')])
    return categories

def get_categories_as_choices():
    return get_categories()

