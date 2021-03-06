import random
from backend.models import UserExtension
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives


def flatten_dict(dct):
    return dict([ (str(k), dct.get(k)) for k in dct.keys() ])


def send_validation_mail_to_user(user_id, email=None, **kwargs):
    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = User.objects.get(id=user_id)
    if user is None:
        return False
    try:
        user_ext = UserExtension.objects.get(user=user)
    except UserExtension.DoesNotExist:
        user_ext = UserExtension.create_from_user(user)
    validation_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in xrange(20)])
    user_ext.validation_code = validation_code
    user_ext.save()
    if email is None:
        email = user.email
    context = {'validation_link': settings.HTTP_BASE_URL + reverse('socialauth.views.validate') + '?id=%s&code=%s' % (user_id, validation_code)}
    return send_email_with_template(settings.EMAIL_HOST_USER,[email],'Welcome to Let\'s Bench', 'email_validation.html', context)

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

def merchant_onreview_email(merchant):
    approvers = User.objects.filter(is_staff=True)
    approver_emails = [str(a.email) for a in approvers]
    send_email_with_template(settings.EMAIL_HOST_USER,approver_emails,'A new application is on review','new_app_review.html',{'merchant':merchant})
    send_email_with_template(settings.EMAIL_HOST_USER,[merchant.user.email],'Your Application is on review', 'app_review.html',{ 'merchant':merchant})

def approve_merchant(merchant):
    merchant.is_approved = True
    merchant.save()
    send_email_with_template(settings.EMAIL_HOST_USER,[merchant.user.email],'Your Application is approved', 'app_approved.html',{ 'merchant':merchant})

def send_email_for_preconfigured_merchant(merchant):
    send_email_with_template(settings.EMAIL_HOST_USER,[merchant.user.email],'Join us', 'preconfigured_merchant.html', {'merchant':merchant})

def send_email_with_template(from_email, to_list, subject, html_file_name, context):
    context['BASE_URL'] = settings.BASE_URL
    c = Context(context)
    html_template = loader.get_template('email_templates/' + html_file_name)
    msg = EmailMultiAlternatives(subject, '', from_email, to_list)
    if html_template is not None:
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
