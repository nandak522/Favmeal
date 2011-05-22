from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponsePermanentRedirect
from utils import response,post_data,_request_param_post,_request_param_get
from utils import login_required,should_be_admin
from django.utils import simplejson

def view_messfood(request, messfood_registration_template, messfood_template):
    selected_maintab = 'messfood'
    if request.user.is_authenticated():
        return response(messfood_template,locals(),request)
    else:
        from messfood.forms import MessFoodRegistrationForm,MessCreationForm
        form = MessFoodRegistrationForm()
        newmessform = MessCreationForm()
        return response(messfood_registration_template,locals(),request)

def view_createmess(request):
    response_dict = {}
    response_dict['errors'] = None
    from messfood.forms import MessCreationForm
    form = MessCreationForm(post_data(request))
    if not form.is_valid():
        response_dict['errors'] = form.errors
        return HttpResponse(simplejson.dumps(response_dict))
    try:
        from common.models import Address
        address = Address.objects.create_address(place=form.cleaned_data.get('mess_place'), landmark=form.cleaned_data.get('mess_landmark'), area=form.cleaned_data.get('mess_area'), zip=form.cleaned_data.get('mess_zip'))
        from messfood.models import Mess
        mess = Mess.objects.create_mess(name=form.cleaned_data.get('mess_place'), address=address)
        response_dict['message']='Your favourite Mess has been put to review'
        response_dict['messname']=mess.name
        response_dict['messid']=mess.id
    except Exception,e:
        response_dict['errors']=e.__str__()
        response_dict['messname']=None
        response_dict['messid']=None
    return HttpResponse(simplejson.dumps(response_dict))
    