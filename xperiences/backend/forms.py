import django.forms as django_forms
from django.forms.widgets import Textarea, DateTimeInput
import settings


class XPDatePicker(DateTimeInput):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'datepicker'
        super(XPDatePicker, self).__init__(attrs=attrs)


    class Media:
        css = {
            'all': ('ui-lightness/jquery-ui-1.8.16.custom.css',)
        }
        js = ('jquery-ui-1.8.16.custom.min.js',)


class RichTextEditorWidget(Textarea):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'ckeditor'
        super(Textarea, self).__init__(attrs=attrs)


    class Media:
        css = {
            'all': ('ckeditor/sample.css',)
        }
        js = ('ckeditor/ckeditor.js', 'ckeditor/sample.js')


def PointWidgetWithAddressField(address_field):
    class PointWidget(django_forms.TextInput):
        def __init__(self, attrs=None):
            attrs = attrs or {}
            attrs['class'] = 'geopicker'
            attrs['address_field'] = address_field
            attrs['style'] = 'display:none;'
            super(PointWidget, self).__init__(attrs=attrs)


        def value_from_datadict(self, data, files, name):
            lat, lng = data.get(name, '0.0,0.0').strip('()').split(',')
            return float(lat), float(lng)


        class Media:
            css = {
                'all': ('map.css',)
            }
            js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js',
                  'https://maps-api-ssl.google.com/maps/api/js?v=3&sensor=false&language=en&libraries=places',
                  'http://www.iplocationtools.com/iplocationtools.js?key=' + settings.IP_GEOLOCATOR_API_KEY,
                  'maps.js')


    return PointWidget

from db_manage import db

def get_all_experiences_as_choices():
    all = db.experience.find({'is_active':True})
    return [(str(e['_id']), str(e['title'])) for e in all]

class SiteConfigurationForm(django_forms.forms.Form):
    CATEGORIES = django_forms.CharField()
    EXPERIENCE_OF_THE_DAY = django_forms.ChoiceField(get_all_experiences_as_choices())

    def __init__(self, data=None):
        from backend import configurations
        if data is None:
            data = configurations.config
        super(SiteConfigurationForm, self).__init__(data)


    def save_data(self):
        from backend import configurations
        configurations.update_configurations(self.data)