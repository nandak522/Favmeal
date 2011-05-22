from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponsePermanentRedirect
from utils import response,post_data,_request_param_post,_request_param_get
from users.decorators import beadashboardadmin
from django.conf import settings

@beadashboardadmin
def view_routes(request, routes_template):
    googlemaps_api_key = settings.GOOGLE_MAPS_API_KEY
    return response(routes_template,locals(),request)