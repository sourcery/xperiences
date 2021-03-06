__author__ = 'ishai'

from django.forms.widgets import Textarea, DateTimeInput
import django.forms as django_forms
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


def PointWidgetWithAddressField(**kwargs):
    class PointWidget(django_forms.TextInput):
        def __init__(self, attrs=None):
            attrs = attrs or {}
            attrs['class'] = 'geopicker'
            attrs['address_field'] = kwargs.get('address_field','')
            attrs['map_id'] = kwargs.get('map_id','')
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
