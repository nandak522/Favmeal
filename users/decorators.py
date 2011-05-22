from django.http import HttpResponseRedirect
from django.core import urlresolvers
from utils.html import _request_param_get

def beadashboardadmin(the_function):
    def _beadashboardadmin(request, *args, **kwargs):
        from django.contrib.auth.models import Group
        dashboard_admin = Group.objects.get(name='admin')
        if dashboard_admin in request.user.groups.all():
            return the_function(request, *args, **kwargs)
        return HttpResponseRedirect('/')
    return _beadashboardadmin