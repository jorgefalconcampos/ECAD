import random
from django.core import mail
from . models import Subscriber, Post
from django.db import IntegrityError
from django.shortcuts import reverse
from . tokens import account_activation_token
from django.core.mail import get_connection, send_mass_mail, EmailMessage
from django.conf import settings as conf_settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from . mailer import SendNewsletterConfirmation, SendConfirmationMail, SendContactMail, SendNewsletterMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



def generate_random_digits():
    return "%0.12d" % random.randint(0, 999999999999)




def mail_newsletterv2(subscriber_email, request):
    rnd = generate_random_digits()
    conf_url ="{}?id={}".format(request.build_absolute_uri('/confirm'), rnd)
    print(f'\n\n# --- PY: Confirmation URL: --- #\n{conf_url}')
    # if 2 users use the same email at the same time (weird scenario, but possible) then the 
    # fastest request will get the confirm email, the second will get an error 
    try:
        sub = Subscriber(email=subscriber_email, conf_num=rnd)
        sub.save()
    except IntegrityError as e:
        if 'UNIQUE constraint' in str(e.args):
            return False

    context = {'email': subscriber_email, 'confirmation_url': conf_url}

    if SendNewsletterConfirmation(subscriber_email, context).send_email():        
        return True
    else:
        sub.delete()
        return False

    
  


def send_activation_linkv2(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = account_activation_token.make_token(user)    
    url_args = reverse('activate', kwargs={ 'uidb64':uid, 'token':token })
    url = request.build_absolute_uri(url_args)
    # context passed to HTML template
    context = {'name': user.first_name, 'username': user.username, 'url':url, 'uid': uid, 'token': token }  
   
    if SendConfirmationMail(user.email, context, first_name=user.first_name, last_name=user.last_name).send_email():
        return True
    else:
        return False


def send_contact_message(context, subject):
    send_to = conf_settings.USERS_HOST_USER
    if SendContactMail(send_to, context, subj=subject).send_email():
        return True
    else:
        return False



def send_newsletter_mail(post, request):
    # getting all the subs and its conf_number, the conf_number must be sent to allow users unsubscribe
    abs_url = request.build_absolute_uri('/')[:-1] # absolute_url
    post_url = '{}{}/{}'.format(f"{abs_url}/post/", post.category.slug, post.slug)
    post_preview = post.post_body
    post_bg_img = '{}{}'.format(abs_url, post.image.url)
    privacy_url = f"{abs_url}/privacy-policy"
    subs = Subscriber.objects.values_list('email', 'conf_num').filter(confirmed=True)
    
    context = {}
    for sub in subs.iterator():
        unsubscribe_url = '{}?id={}'.format(f"{abs_url}/unsubscribe", sub[1])
        context[sub[0]] = unsubscribe_url

    # To delete later (maybe) - START
    subscribers = []
    print(f'\n\n# --- PY: List of all subscribers email: --- #\n')
    for (i, element) in enumerate([i[0] for i in subs], start=1):
        subscribers.append(element)
        print(f'> {i}: {element}')

    if SendNewsletterMessage(subscribers, context, index_url=abs_url, post_title=post.title, post_url=post_url, post_preview=post_preview, post_bg_img=post_bg_img, privacy_url=privacy_url).send_massive_email():
        return True
    else:
        return False