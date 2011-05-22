from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from utils import response, post_data, _request_param_post, _request_param_get
from utils import _add_noticemsg, _add_errormsg, _add_successmsg
from django.conf import settings
from django.core import urlresolvers

def view_login(request, login_template):
    selected_maintab = 'login'
    if request.method != 'POST':
        from users.forms import LoginForm
        loginform = LoginForm()
        return response(login_template,locals(),request)
    from users.forms import LoginForm
    loginform = LoginForm(post_data(request))
    if loginform.is_valid():
        email = loginform.cleaned_data.get('lusername')
        password = loginform.cleaned_data.get('lpassword')
        from utils import setup_loggedin_environment
        user = setup_loggedin_environment(request, email, password)
        if not user:
            from users.messages import INVALID_LOGIN_INFO
            _add_errormsg(request, INVALID_LOGIN_INFO)
            return response(login_template,locals(),request)
        from utils import get_post_login_url
        post_login_url = get_post_login_url(user.get_profile())
        return HttpResponseRedirect(post_login_url)
    return response(login_template,locals(),request)

def view_logout(request):
    user = request.user
    if user.is_authenticated():
        from django.contrib.auth import logout
        logout(request)
    return HttpResponseRedirect('/')