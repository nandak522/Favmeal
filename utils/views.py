from utils import response
from django.conf import settings

def handle404(request):
    return response(settings.TEMPLATE_404,locals(),request)