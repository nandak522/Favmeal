from django.template import loader
from django.conf import settings
from django.core.mail import send_mail as default_django_emailer

def customer_query_emailer(subject,from_email,email_body,from_name=''):
    return default_django_emailer(subject, "From:<%s>%s\n%s" % (from_name,from_email,email_body), "<%s>%s" % ('nandakishore',from_email),['contact@favmeal.com'], fail_silently=False)

def mail_admins(exception,params):
    return default_django_emailer('Exception', "Reason:%s\nParams:%s" % (exception.__str__(),str(params)), 'do-not-reply@favmeal.com',['nandakishore@favmeal.com'], fail_silently=False)

def passwordreset_mailer(userprofile, new_password):
    from crons.models import Job
    args = {'email':str(userprofile.email).strip(),'password':str(new_password).strip()}
    Job.objects.add_job('W',_action(send_password_reset_mail),args,userprofile)

def send_password_reset_mail(userprofile,args):
    email=args['email']
    password=args['password']
    send_email('Password Recovery', userprofile.name,email,locals(), 'emails/passwordreset.html',"<Favmeal>%s" % settings.DEFAULT_FROM_EMAIL)
    
def send_email(subject,name,email,context,template,sender=settings.DEFAULT_FROM_EMAIL):
    if settings.REDIRECT_EMAILS:
        print 'Emails to %s are redirected to %s' % (email, settings.EMAIL_TESTER)
        email = settings.EMAIL_TESTER
    message = loader.render_to_string(template, context) 
    default_django_emailer(subject, message, sender, [email], fail_silently = False)
    
def _action(method):
    return str(method.__module__+"."+method.__name__)    