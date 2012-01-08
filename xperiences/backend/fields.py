import lxml.html
from django.db import models
from django.forms.fields import CharField
from django_mongodb_engine.contrib import MongoDBManager
from djangotoolbox.fields import EmbeddedModelField, ListField
from backend.widgets import PointWidgetWithAddressField, RichTextEditorWidget
from sorl.thumbnail import ImageField

DEFAULT_MAX_DISTANCE = 1500

class XPDBManager(MongoDBManager):
    def proximity_query(self, location, **kwargs):
        max_distance = float(kwargs.get('max_distance', DEFAULT_MAX_DISTANCE/10))
        field_name = kwargs.get('field', 'xp_location')
        lat = location['lat']
        lng = location['lng']
        query = kwargs.get('query', {})
        query[field_name] = {'$near': {'lat': lat, 'lng': lng},'$maxDistance':max_distance}
        return self.raw_query(query)

    def text_search(self, keyword, **kwargs):
        query = kwargs.get('query', {})
        query['keywords'] = keyword
        return self.raw_query(query)


class Coordinate(models.Model):
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    geom_type = 'POINT'


    def __str__(self):
        return '%f,%f' % (self.lat, self.lng)


class GeoField(EmbeddedModelField):
    address_field = ''
    map_id = ''

    def __init__(self, **kwargs):
        kwargs['default'] = Coordinate
        #        kwargs['editable'] = False
        if 'address_field' in kwargs:
            self.address_field = 'id_' + kwargs.pop('address_field')
        if 'map_id' in kwargs:
            self.map_id = kwargs.pop('map_id')
        super(GeoField, self).__init__(Coordinate, **kwargs)


    def formfield(self, **kwargs):
    # A file widget is provided, but use model FileField or ImageField
        # for storing specific files most of the time
        defaults = {'widget': PointWidgetWithAddressField(address_field=self.address_field)}
        #        attrs = kwargs.get('attrs',{})
        #        attrs['address_field'] = self.address_field
        defaults.update(kwargs)
        #        defaults['attrs'] = attrs
        return super(GeoField, self).formfield(self.FormClass, **defaults)


    class FormClass(CharField):
        def to_python(self, (lat, lng)):
            return Coordinate(lat=lat, lng=lng)

# The reason I changed TextField to CharField was to avoid that text area it
# creating in the add_experience form. However, I am not sure how it's going
# affect search... I guess it needs to be TextField to be searchable?
class TextSearchField(models.CharField):
    def get_text(self, instance):
        return getattr(instance, self.name)


class RichTextField(TextSearchField):
    def __init__(self, **kwargs):
        defaults = {'max_length': 4096}
        defaults.update(kwargs)
        super(RichTextField, self).__init__(**defaults)


    def get_text(self, instance):
        s = getattr(instance, self.name)
        if not s:
            return None
        t = lxml.html.fromstring(getattr(instance, self.attname, ''))
        return t.text


    def formfield(self, **kwargs):
        kwargs['widget'] = RichTextEditorWidget
        return super(RichTextField, self).formfield(**kwargs)


class XPImageField(ImageField):
    thumbnail_size = None


    def __init__(self, *args, **kwargs):
        self.thumbnail_size = kwargs.get('thumbnail_size', (450, 300))
        if 'thumbnail_size' in kwargs:
            del kwargs['thumbnail_size']
        super(XPImageField, self).__init__(*args, **kwargs)


    def thumbnail_size_str(self):
        return '%dx%d' % self.thumbnail_size


_FULL_TEXT_STOP_WORDS = frozenset([
    'a', 'about', 'according', 'accordingly', 'affected', 'affecting', 'after',
    'again', 'against', 'all', 'almost', 'already', 'also', 'although',
    'always', 'am', 'among', 'an', 'and', 'any', 'anyone', 'apparently', 'are',
    'arise', 'as', 'aside', 'at', 'away', 'be', 'became', 'because', 'become',
    'becomes', 'been', 'before', 'being', 'between', 'both', 'briefly', 'but',
    'by', 'came', 'can', 'cannot', 'certain', 'certainly', 'could', 'did', 'do',
    'does', 'done', 'during', 'each', 'either', 'else', 'etc', 'ever', 'every',
    'following', 'for', 'found', 'from', 'further', 'gave', 'gets', 'give',
    'given', 'giving', 'gone', 'got', 'had', 'hardly', 'has', 'have', 'having',
    'here', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'itself',
    'just', 'keep', 'kept', 'knowledge', 'largely', 'like', 'made', 'mainly',
    'make', 'many', 'might', 'more', 'most', 'mostly', 'much', 'must', 'nearly',
    'necessarily', 'neither', 'next', 'no', 'none', 'nor', 'normally', 'not',
    'noted', 'now', 'obtain', 'obtained', 'of', 'often', 'on', 'only', 'or',
    'other', 'our', 'out', 'owing', 'particularly', 'past', 'perhaps', 'please',
    'poorly', 'possible', 'possibly', 'potentially', 'predominantly', 'present',
    'previously', 'primarily', 'probably', 'prompt', 'promptly', 'put',
    'quickly', 'quite', 'rather', 'readily', 'really', 'recently', 'regarding',
    'regardless', 'relatively', 'respectively', 'resulted', 'resulting',
    'results', 'said', 'same', 'seem', 'seen', 'several', 'shall', 'should',
    'show', 'showed', 'shown', 'shows', 'significantly', 'similar', 'similarly',
    'since', 'slightly', 'so', 'some', 'sometime', 'somewhat', 'soon',
    'specifically', 'state', 'states', 'strongly', 'substantially',
    'successfully', 'such', 'sufficiently', 'than', 'that', 'the', 'their',
    'theirs', 'them', 'then', 'there', 'therefore', 'these', 'they', 'this',
    'those', 'though', 'through', 'throughout', 'to', 'too', 'toward', 'under',
    'unless', 'until', 'up', 'upon', 'use', 'used', 'usefully', 'usefulness',
    'using', 'usually', 'various', 'very', 'was', 'we', 'were', 'what', 'when',
    'where', 'whether', 'which', 'while', 'who', 'whose', 'why', 'widely',
    'will', 'with', 'within', 'without', 'would', 'yet', 'you'])


class XPModel(models.Model):
    objects = XPDBManager()


    class Meta:
        abstract = True


class TextSearchModel(XPModel):
    keywords = ListField(editable=False)
    originals = {}


    def __init__(self, *args, **kwargs):
        super(TextSearchModel, self).__init__(*args, **kwargs)
        for field in self._meta.fields:
            if isinstance(field, TextSearchField):
                self.originals[field.name] = getattr(self, field.name)


    def save(self, *args, **kwargs):
        # process text fields
        fields = self._meta.fields
        is_changed = False
        all_text = []
        for field in fields:
            if isinstance(field, TextSearchField):
                value = field.get_text(self)
                if self.originals[field.name] != value:
                    is_changed = True
                if value:
                    all_text.append(value)
        if is_changed:
            all_words = {}
            for text in all_text:
                words = text.split(' ')
                for word in words:
                    word = word.strip()
                    word = word.lower()
                    if word != '' and word not in _FULL_TEXT_STOP_WORDS:
                        all_words[word] = True
            all_words_list = all_words.keys()
            self.keywords = all_words_list
        obj = super(TextSearchModel, self).save(*args, **kwargs)
        return obj


    class Meta:
        abstract = True


class GeoModel(XPModel):
    xp_location = GeoField(address_field='address')
    address = models.CharField(max_length=100, default='', blank=True)


    def update_location(self, arg_lat, arg_lng):
        self.xp_location.lat = arg_lat
        self.xp_location.lng = arg_lng


    class Meta:
        abstract = True
