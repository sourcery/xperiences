import random
from backend.models import UserExtension
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import settings

__author__ = 'ishai'

from django.template import loader, Context
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def flatten_dict(dct):
    return dict([ (str(k), dct.get(k)) for k in dct.keys() ])


def send_validation_mail_to_user(user_id, email=None, **kwargs):
    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = User.objects.get(id=user_id)
    if user == None:
        return False
    try:
        user_ext = UserExtension.objects.get(user=user)
    except UserExtension.DoesNotExist:
        user_ext = UserExtension.create_from_user(user)
    validation_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in xrange(20)])
    user_ext.validation_code = validation_code
    user_ext.save()
    if email == None:
        email = user.email
    context = {'validation_link': settings.HTTP_BASE_URL + reverse('socialauth.views.validate') + '?id=%s&code=%s' % (user_id, validation_code)}
    return send_email_with_template(settings.EMAIL_HOST_USER,[email],'Welcome to Let\'s Bench', 'email_validation.txt', 'email_validation.html', context)

def validate_user(user_id, code):
    user = User.objects.get(id=user_id)
    if user.is_active:
        return True
    user_ext = UserExtension.objects.get(user=user)
    if user_ext.validation_code == code:
        user.is_active = True
        user.save()
        return True
    return False

def send_email_with_template(from_email, to_list, subject, text_file_name, html_file_name, context):
    c = Context(context)
    text_template = loader.get_template('email_templates/' + text_file_name)
    html_template = loader.get_template('email_templates/' + html_file_name)
    if text_template == None:
        return False

    text_content = text_template.render(c)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
    if html_template != None:
        html_content = html_template.render(c)
        msg.attach_alternative(html_content, "text/html")
    return msg.send() > 0

BUFFER_SIZE = 1500

def read_urllib_fp_to_str(fp):
    str = ''
    info = fp.info()
    length = 0
    for header in info.headers:
        header = header.lower()
        parts =  header.split('content-length: ')
        if len(parts) > 1:
            length = int(parts[1])
    seek = 0
    while seek < length:
       to_read = min(BUFFER_SIZE, length - seek)
       seek += to_read
       str += fp.read(to_read)
    return str
