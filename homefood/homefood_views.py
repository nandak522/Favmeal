from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from utils import response, post_data, _request_param_post, _request_param_get
from utils import _add_noticemsg, _add_errormsg, _add_successmsg
from django.conf import settings

def view_homefood(request,homefood_registration_template,homefood_template):
    selected_maintab = 'homefood'
    if request.user.is_authenticated():
        googlemaps_api_key = None
        if settings.MAPPING_ENABLED:
            googlemaps_api_key = settings.GOOGLE_MAPS_API_KEY
        return response(homefood_template,locals(),request)
    else:
        from homefood.forms import HomeFoodRegistrationForm
        form = HomeFoodRegistrationForm()
        return response(homefood_registration_template,locals(),request)

