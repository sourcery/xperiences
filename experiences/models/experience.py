from django.template.defaultfilters import slugify 

def slug(e):
    """accepts experience dictionary and returns a string which is the slugified version of
        the experience's title.
    """
    return slugify(e['title'])