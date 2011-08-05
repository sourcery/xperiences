from django.template.defaultfilters import slugify 

def slug(m):
    """accepts merchant dictionary and returns a string which is the slugified version of
        the merchant's username.
    """
    return slugify(m['name'])