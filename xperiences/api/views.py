from backend import utils
import settings

__author__ = 'ishai'

def test(request):
    utils.send_email_with_template(settings.EMAIL_HOST_USER,['ishaijaffe84@gmail.com'],'xperiences test','empty.html',{'content':request})
  