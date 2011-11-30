from django.forms import forms as django_forms
from django.forms.widgets import Textarea


class RichTextEditorWidget(Textarea):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'ckeditor'
        super(Textarea, self).__init__(attrs=attrs)

    class Media:
        css = {
            'all' : ('ckeditor/sample.css',)
        }
        js = ('ckeditor/ckeditor.js','ckeditor/sample.js')

def PointWidgetWithAddressField(address_field):
    class PointWidget(django_forms.TextInput):

        def __init__(self, attrs=None):
            attrs = attrs or {}
            attrs['class'] = 'geopicker'
            attrs['address_field'] = address_field
            super(PointWidget, self).__init__(attrs=attrs)

        def value_from_datadict(self, data, files, name):
            lat,lng =  data.get(name,'0.0,0.0').split(',')
            return (float(lat), float(lng))

        class Media:
            css = {
                'all' : ('map.css',)
            }
            js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js','https://maps-api-ssl.google.com/maps/api/js?v=3&sensor=false&language=he&libraries=places','maps.js')
    return PointWidget

