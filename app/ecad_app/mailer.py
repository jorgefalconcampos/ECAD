from django.core import mail #EmailMessage lives here
from django.utils.text import format_lazy as fl
from django.conf import settings as conf_settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail, get_connection, send_mass_mail



class BaseMassiveMailer():
    def __init__(self, message_to, context, subject, template, sndr_host, sndr_username, sndr_pass, sndr_port, sndr_tls, **substitutions):

        self.con = mail.get_connection()

        self.subject = subject
        self.message_to = message_to #A list of emails

        self.template = template
        self.context = context
        
        self.sndr_host = sndr_host
        self.sndr_port = sndr_port
        self.sndr_username = sndr_username
        self.sndr_pass = sndr_pass
        self.sndr_tls = sndr_tls

        self.substitutions = { }

        for key in substitutions:
            self.substitutions.update({key:substitutions[key]})


    def create_emails(self):
        try: 
            # creating connection
            self.con.open()

            #filling the connection (EmailBackend) object
            self.mail_obj = EmailBackend(
                host=self.sndr_host, 
                port=self.sndr_port,
                username=self.sndr_username,
                password=self.sndr_pass,
                use_tls=self.sndr_tls)

            self.mails = []

            # filling the EmailMessage objects
            for email in self.message_to:
                for k,v in self.context.items():
                    if k == email:   
                        ctxt = {
                            'email':k, 
                            'unsubscribe_url':v, 
                            'index_url':self.substitutions["index_url"],
                            'post_title':self.substitutions["post_title"],
                            'post_url':self.substitutions["post_url"],
                            'post_preview':self.substitutions["post_preview"],
                            'post_bg_img':self.substitutions["post_bg_img"],
                            'privacy_url':self.substitutions["privacy_url"],}
                        body_msg = render_to_string(self.template, ctxt)
                        new_mail_msg = mail.EmailMessage(
                            subject=self.subject, 
                            body=body_msg, 
                            from_email=self.sndr_username,
                            to=[email],
                            connection=self.con)
                        
                        self.mails.append(new_mail_msg)

        except Exception as e:
            print(f'\n\n# --- PY: Error while creating the connection or mail(s) message(s): --- #\n{e}')


    def send_massive_email(self):
        self.create_emails()
        try:
            for mail in self.mails:
                mail.content_subtype = 'html'
            self.mail_obj.send_messages(self.mails)
            self.con.close()
            return True
        except Exception as e:
            print(f'\n\n# --- PY: Error sending massive emails: --- #\n{e}')
            return False



class BaseMailer():
    def __init__(self, message_to, context, subject, template, sndr_host, sndr_port, sndr_username, sndr_pass, sndr_tls, **substitutions):

        self.con = mail.get_connection()

        self.message_to = message_to
        self.subject = subject
        self.body_msg = render_to_string(template, context)
        
        self.sndr_host = sndr_host
        self.sndr_port = sndr_port
        self.sndr_username = sndr_username
        self.sndr_pass = sndr_pass
        self.sndr_tls = sndr_tls

        # sth like request o algo asi xd
        self.substitutions = {}

        for key in substitutions:
            self.substitutions.update({key:substitutions[key]})


    def create_email(self):
        try:
            # creating connection
            self.con.open()

            #filling the connection (EmailBackend) object
            self.mail_obj = EmailBackend(
                host=self.sndr_host, 
                port=self.sndr_port,
                username=self.sndr_username,
                password=self.sndr_pass,
                use_tls=self.sndr_tls)

            # filling the EmailMessage object
            self.mail = mail.EmailMessage(
                subject=self.subject, 
                body=self.body_msg, 
                from_email=self.sndr_username,
                to=[self.message_to],
                connection=self.con)
        
        except Exception as e:
            print(f'\n\n# --- PY: Error while creating the connection or mail(s) message(s): --- #\n{e}')
  

    def send_email(self):
        self.create_email()
        try:
            self.mail.content_subtype = 'html'
            self.con.send_messages([self.mail]) #sending email with the current connection, this is intended to send messages to multiple mails w/ the same conn
            # self.mail.send(self.mail) #sending email with the EmailMessage object
            # self.mail_obj.send_messages([self.mail]) #sending email with EmailBackend
            self.con.close()
            return True
        except Exception as e:
            print(f'\n\n# --- PY: Error sending email: --- #\n{e}')
            return False



class SendNewsletterConfirmation(BaseMailer):
    def __init__(self, message_to, context, **substitutions):
        super().__init__(
            message_to, 
            context,
            subject = _('str_confirmYourEmail'), 
            template = 'ecad_app/mails/blog/confirm-mail.html',
            sndr_host = conf_settings.EMAIL_HOST, 
            sndr_port = conf_settings.EMAIL_PORT,
            sndr_username = conf_settings.NEWSLETTER_HOST_USER, 
            sndr_pass = conf_settings.NEWSLETTER_HOST_PASSWORD, 
            sndr_tls = conf_settings.EMAIL_USE_TLS,
            **substitutions
            )



class SendConfirmationMail(BaseMailer):
    def __init__(self, message_to, context, **substitutions):
        super().__init__(
            message_to,
            context,
            subject = fl('{} {} {}', _('str_mails_activationMail4'), substitutions["first_name"], substitutions["last_name"]),
            template = 'ecad_app/mails/user/activate-email.html',
            sndr_host = conf_settings.EMAIL_HOST,
            sndr_username = conf_settings.USERS_HOST_USER, 
            sndr_pass = conf_settings.USERS_HOST_PASSWORD, 
            sndr_port = conf_settings.EMAIL_PORT,
            sndr_tls = conf_settings.EMAIL_USE_TLS,
            **substitutions
            )



class SendContactMail(BaseMailer):
    def __init__(self, message_to, context, **substitutions):
        super().__init__(
            message_to,
            context,
            subject = fl('{}: {}', _('str_mails_newMail'), substitutions["subj"]),
            template = 'ecad_app/user/contact-mail.html',
            sndr_host = conf_settings.EMAIL_HOST,
            # ---- change only username and pass
            sndr_username = conf_settings.CONTACT_HOST_USER, 
            sndr_pass = conf_settings.CONTACT_HOST_PASSWORD, 
            # change only username and pass ----
            sndr_port = conf_settings.EMAIL_PORT,
            sndr_tls = conf_settings.EMAIL_USE_TLS,
            **substitutions
            )



class SendNewsletterMessage(BaseMassiveMailer):
    def __init__(self, message_to, context, **substitutions):
        super().__init__(
            message_to, 
            context,
            subject = fl('{}: {}', _('str_mails_newsletterNewMail'), substitutions["post_title"]),
            template = 'ecad_app/mails/blog/avg-mail.html',
            sndr_host = conf_settings.EMAIL_HOST,
            sndr_username = conf_settings.NEWSLETTER_HOST_USER, 
            sndr_pass = conf_settings.NEWSLETTER_HOST_PASSWORD, 
            sndr_port = conf_settings.EMAIL_PORT,
            sndr_tls = conf_settings.EMAIL_USE_TLS,
            **substitutions
            )

