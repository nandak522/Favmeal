from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test as django_login_required
from django.http import Http404
from django.core import urlresolvers

def response(template, params={}, request=None):
    if request:
        return render_to_response(template, params, context_instance=RequestContext(request))
    return render_to_response(template, params)

def post_data(request):
    return request.POST.copy()

def _request_param_post(request,key):
    if request.POST.has_key(key):
        return request.POST.get(key)
    else:
        return None
    
def _request_param_get(request,key):
    if request.GET.has_key(key):
        return request.GET.get(key)
    else:
        return None    
    
def name_for_linking(name):
    from utils.html import clean, clean_html_tags
    def _allowed(c):
        if c.isalnum(): return True
        if c in [' ', '-', '_']: return True
        return False
    return filter(_allowed, clean_html_tags(name.strip())).strip().replace(" ", "-")

def should_be_admin(the_function):
    def _should_be_admin(request, *args, **kwargs):
        if request.user.is_anonymous():
            raise Http404
        from django.contrib.auth.models import Group
        if Group.objects.get(name='admin') in request.user.groups.all():
            return the_function(request, *args, **kwargs)
#        if request.user.is_superuser: return the_function(request, *args, **kwargs)
        raise Http404
    return _should_be_admin

auth_check = lambda u : u.is_authenticated()
login_required = django_login_required(auth_check, login_url= '/login/')


CENTERALIGNMSG="<div style=\'text-align:center;font:bold 1em sans-serif;\'>%s</div>"
def _add_noticemsg(request,reminder,align_center=True):
    if align_center:
        reminder=CENTERALIGNMSG%(reminder)
    request.fmessages.add_reminder_msg(reminder)
    
def _add_errormsg(request,errormsg,align_center=True):
    if align_center:
        errormsg=CENTERALIGNMSG%(errormsg)
    request.fmessages.add_error_msg(errormsg)

def _add_successmsg(request,msg,align_center=True):
    if align_center:
        msg=CENTERALIGNMSG%(msg)
    request.fmessages.add_msg(msg)

def setup_loggedin_environment(request, email, password):
    from django.contrib.auth import authenticate, login
    authenticated_user = authenticate(username=email, password=password)
    if not authenticated_user:
        return None
    login(request, authenticated_user)
    return authenticated_user

def get_next_param(request):
    if _request_param_get(request,'next'):
        return _request_param_get(request,'next')
    elif _request_param_post(request,'next'):
        return _request_param_post(request,'next')
    return None

def get_post_login_url(userprofile):
    service_type = userprofile.get_service_type()
    if service_type == 'homefood':
        return urlresolvers.reverse('homefood.views.view_homefood')
    if service_type == 'restaurantfood':
        return urlresolvers.reverse('restaurants.views.view_restaurants')
    if service_type == 'messfood':
        return urlresolvers.reverse('messfood.views.view_messfood')
    return '/'

def load_module(path):
    module_path = path.split('.')
    # Allow for Python 2.5 relative paths
    if len(module_path) > 1:
        module_name = '.'.join(module_path[:-1])
    else:
        module_name = '.'
    module = __import__(module_name, globals(), {}, module_path[-1])
    the_object = getattr(module, module_path[-1])
    return the_object