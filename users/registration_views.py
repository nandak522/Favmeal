from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from utils import response, post_data, _request_param_post, _request_param_get
from utils import _add_noticemsg, _add_errormsg, _add_successmsg
from django.conf import settings
from django.core import urlresolvers

def view_register(request, homefood_registration_template, restaurantfood_registration_template, messfood_registration_template):
    if request.method != 'POST':
        return HttpResponseRedirect('/')
    service_type = _request_param_post(request, 'service_type')
    if not service_type:
        return HttpResponseRedirect('/')
    if service_type == 'homefood':
        return _proceed_to_homefood_registration(request, homefood_registration_template)
    elif service_type == 'restaurantfood':
        return _proceed_to_restaurantfood_registration(request, restaurantfood_registration_template)
    elif service_type == 'messfood':
        return _proceed_to_messfood_registration(request, messfood_registration_template)
    return HttpResponseRedirect('/')

def _proceed_to_homefood_registration(request, registration_template):
    selected_maintab = 'homefood'
    from homefood.forms import HomeFoodRegistrationForm
    form = HomeFoodRegistrationForm(post_data(request))
    if form.is_valid():
        userprofile = _do_register(request, form)
        from utils import setup_loggedin_environment
        setup_loggedin_environment(request, userprofile.email, password=form.cleaned_data.get('rpassword'))
        from utils import get_post_login_url
        post_login_url = get_post_login_url(userprofile)
        return HttpResponseRedirect(post_login_url)
    return response(registration_template, locals(), request)

def _proceed_to_restaurantfood_registration(request, registration_template):
    selected_maintab = 'restaurantfood'
    from restaurants.forms import RestaurantFoodRegistrationForm
    form = RestaurantFoodRegistrationForm(post_data(request))
    if form.is_valid():
        userprofile = _do_register(request, form)
        from utils import setup_loggedin_environment
        setup_loggedin_environment(request, userprofile.email, password=form.cleaned_data.get('rpassword'))
        from utils import get_post_login_url
        post_login_url = get_post_login_url(userprofile)
        return HttpResponseRedirect(post_login_url)
    return response(registration_template, locals(), request)

def _proceed_to_messfood_registration(request, registration_template):
    from messfood.models import Mess
    selected_maintab = 'messfood'
    from messfood.forms import MessFoodRegistrationForm,MessCreationForm
    form = MessFoodRegistrationForm(post_data(request))
    newmessform = MessCreationForm()
    if form.is_valid():
        userprofile = _do_register(request, form)
        from utils import setup_loggedin_environment
        setup_loggedin_environment(request, userprofile.email, password=form.cleaned_data.get('rpassword'))
        from utils import get_post_login_url
        post_login_url = get_post_login_url(userprofile)
        return HttpResponseRedirect(post_login_url)
    return response(registration_template, locals(), request)

def _do_register(request, form):
    email = form.cleaned_data.get('remail')
    password = form.cleaned_data.get('rpassword')
    mobile = form.cleaned_data.get('mobile')
    service_type = form.cleaned_data.get('service_type')
    source_place = ''
    source_area = ''
    source_landmark = ''
    source_zip = ''
    if service_type == 'homefood':
        source_place = form.cleaned_data.get('home_place')
        source_area = form.cleaned_data.get('home_area')
        source_landmark = form.cleaned_data.get('home_landmark')
        source_zip = form.cleaned_data.get('home_zip')
    elif service_type == 'messfood':
        from messfood.models import Mess
        mess = Mess.objects.get(id=int(form.cleaned_data.get('mess')))
        source_place = mess.address.place
        source_area = mess.address.area
        source_landmark = mess.address.landmark
        source_zip = mess.address.zip
    destination_place = form.cleaned_data.get('office_place')
    destination_area = form.cleaned_data.get('office_area')
    if destination_area == '-1':
        destination_area = form.cleaned_data.get('office_other_area')
    else:
        for available_destination in settings.SERVICE_AVAILABLE_DESTINATIONS:
            if available_destination[0] == int(form.cleaned_data.get('office_area')):
                destination_area = available_destination[1]
                break
    destination_landmark = form.cleaned_data.get('office_landmark')
    destination_zip = form.cleaned_data.get('office_zip')
    city = 'Hyderabad'
    from users.models import UserProfile
    userprofile = UserProfile.objects.create_userprofile(email=email,
                                                         password=password,
                                                         service_type=service_type,
                                                         mobile=mobile,
                                                         source_place=source_place,
                                                         source_area=source_area,
                                                         source_landmark=source_landmark,
                                                         source_zip=source_zip,
                                                         destination_place=destination_place,
                                                         destination_area=destination_area,
                                                         destination_landmark=destination_landmark,
                                                         destination_zip=destination_zip)
    return userprofile
        
def view_checkemail(request):
    remail = _request_param_post(request, 'remail')
    if not remail:
        from users.messages import ICON_CROSS, INVALID_EMAIL_ADDRESS_ERROR_MESSAGE
        return HttpResponse('%s%s' % (ICON_CROSS, INVALID_EMAIL_ADDRESS_ERROR_MESSAGE))
    from django.forms.fields import email_re
    if not email_re.search(remail.strip().lower()):
        from users.messages import ICON_CROSS, INVALID_EMAIL_ADDRESS_ERROR_MESSAGE
        return HttpResponse('%s%s' % (ICON_CROSS, INVALID_EMAIL_ADDRESS_ERROR_MESSAGE))
    from users.models import UserProfile
    if UserProfile.objects.filter(email=remail):
        from users.messages import ICON_CROSS, EMAIL_ADDRESS_ALREADY_TAKEN_ERROR_MESSAGE
        return HttpResponse('%s%s' % (ICON_CROSS, EMAIL_ADDRESS_ALREADY_TAKEN_ERROR_MESSAGE))
    else:
        from users.messages import ICON_SUCESS, VALID_EMAIL_ADDRESS_MESSAGE
        return HttpResponse('%s%s' % (ICON_SUCESS, VALID_EMAIL_ADDRESS_MESSAGE))