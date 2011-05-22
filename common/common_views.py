from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from utils import response, post_data, _request_param_post, _request_param_get
from utils import _add_noticemsg, _add_errormsg, _add_successmsg
from django.conf import settings
from django.core import urlresolvers

def view_contactus(request,homepage_template,contactus_template):
    selected_maintab = 'contactus'
    if request.method != 'POST':
        from common.forms import ContactUsQueryForm
        form = ContactUsQueryForm()
        return response(contactus_template, locals(), request)
    from common.forms import ContactUsQueryForm
    form = ContactUsQueryForm(post_data(request))
    if not form.is_valid():
        return response(contactus_template, locals(), request)
    email = form.cleaned_data.get('email')
    name = form.cleaned_data.get('name')
    query = form.cleaned_data.get('query')
    from utils.emailer import customer_query_emailer
    mail_sent = customer_query_emailer(subject="Customer Query",from_email=email,email_body=query,from_name=name)
    if mail_sent:
        _add_successmsg(request,'Query Successfully Submitted. We will get back to you very soon. Thankyou.')
        return response(homepage_template, locals(), request)
    _add_errormsg(request,'Query can\'t be submitted now. Please try again.')
    return response(contactus_template, locals(), request)

def view_refer_friend(request, referfriend_template):
    if request.method != 'POST':
        from common.forms import ReferFriendForm
        form = ReferFriendForm()
        return response(referfriend_template, locals(), request)
    from common.forms import ReferFriendForm
    form = ReferFriendForm(post_data(request))
    if not form.is_valid():
        _add_errormsg(request,'Please fill up valid inforsettingsmation in required fields')
        return response(referfriend_template, locals(), request)
    name = form.cleaned_data.get('name')
    email = form.cleaned_data.get('email')
    ref_emails = form.cleaned_data.get('ref_emails')
    ref_mobiles = form.cleaned_data.get('ref_mobiles')
    if _send_invitations(request,name, email, ref_emails, ref_mobiles):
        _add_successmsg(request, 'Your friend(s) \' %s \' have been invited. Thanks for being with favmeal!' % (ref_emails))
        return response(referfriend_template, locals(), request)        
    else:
        _add_errormsg(request,'There seems to be a problem in sending the invitation. Please try again!')
        return response(referfriend_template, locals(), request)        

def _send_invitations(request,name, email, ref_emails, ref_mobiles):
    datalist = []
    referfriend_mail_sub = "Do you know about Favmeal?"
    all_emails_list = ref_emails.strip().split(',')
    try:
        from django.core.mail import send_mail, EmailMessage
        from django.template.loader import render_to_string
        html_content = render_to_string('referfriend_mail_content.html', {name:name})
        
        if name:
            from_email = '%s<%s>' % (name, email)
        else:
            from_email = '%s<%s>' % (email, email)
        for to_email in all_emails_list:
            msg = EmailMessage(referfriend_mail_sub, html_content, from_email, [to_email])
            msg.content_subtype = "html"
            msg.attach_file(settings.MEDIA_ROOT+'flat/Favmeal_Brochure.pdf')
            all_invited = msg.send(fail_silently=False)
        #FIXME:Refactor the below code
        admin_mail_sub = "[Refer Friend] By %s<%s>" % (name,email)
        admin_mail_body = "From: %s<%s>\nReferred email Ids: %s; Referred Mobiles: %s" % (name,email,ref_emails,ref_mobiles)
        admin_mail_sent = send_mail(admin_mail_sub, admin_mail_body, '',['contact@favmeal.com'], fail_silently=False)
    except Exception,e:
        #FIXME:Avoid global Exceptions. Have proper handling mechanism for each case
        _add_errormsg(request,'We are facing difficulty with mail servers. Please try again.')
        return False
    if all_invited: 
		return admin_mail_sent
    else: 
		return all_invited
