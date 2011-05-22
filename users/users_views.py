from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from utils import response, post_data, _request_param_post, _request_param_get
from utils import should_be_admin, login_required
from utils import _add_noticemsg, _add_errormsg, _add_successmsg
from django.contrib.auth.decorators import login_required as django_login_required

def view_homepage(request, homepage_template):
    selected_maintab = 'home'
    return response(homepage_template, locals(), request)

@should_be_admin#FIXME:for now enabled to admin, later should be enabled to everybody
def view_userdashboard(request,userdashboard_template):
    return response(userdashboard_template,locals(),request)

@login_required
def view_account(request,account_template):
    selected_maintab = 'account'
    userprofile = request.user.get_profile()
    if request.method !='POST':
        from users.forms import AccountForm
        accountform = AccountForm({'mobile':userprofile.mobile,
                                   'home_place':userprofile.source.place,'home_landmark':userprofile.source.landmark,'home_area':userprofile.source.area,'home_zip':userprofile.source.zip,
                                   'office_place':userprofile.destination.place,'office_landmark':userprofile.destination.landmark,'office_area':userprofile.destination.area,'office_zip':userprofile.destination.zip})
        return response(account_template,locals(),request)
    else:
        if userprofile.get_service_type() == 'homefood':
            return _process_homefood_account_information(userprofile,request,account_template)
        if userprofile.get_service_type() == 'restaurantfood':
            return _process_restfood_account_information(userprofile,request,account_template)
        if userprofile.get_service_type() == 'messfood':
            return _process_messfood_account_information(userprofile,request,account_template)

def _process_homefood_account_information(userprofile,request,account_template):
    from users.forms import AccountForm
    accountform = AccountForm(post_data(request))
    if not accountform.is_valid():
        _add_errormsg(request, 'Please valid information in all the required fields')
        return response(account_template,locals(),request)
    password = accountform.cleaned_data.get('password')
    userprofile.set_password(password)
    mobile = accountform.cleaned_data.get('mobile')
    userprofile.mobile = mobile
    home_place = accountform.cleaned_data.get('home_place')
    home_landmark = accountform.cleaned_data.get('home_landmark')
    home_area = accountform.cleaned_data.get('home_area')
    home_zip = accountform.cleaned_data.get('home_zip')
    userprofile.set_source_address(source_place=home_place,source_area=home_area,source_landmark=home_landmark,source_zip=home_zip)
    office_place = accountform.cleaned_data.get('office_place')
    office_landmark = accountform.cleaned_data.get('office_landmark')
    office_area = accountform.cleaned_data.get('office_area')
    office_zip = accountform.cleaned_data.get('office_zip')
    userprofile.set_destination_address(destination_place=office_place,destination_area=office_area,destination_landmark=office_landmark,destination_zip=office_zip)
    _add_successmsg(request, 'Account Information saved Successfully')
    return response(account_template,locals(),request)
    
def _process_restfood_account_information(userprofile,request,account_template):
    password = _request_param_post(request, 'password')
    mobile = _request_param_post(request, 'mobile')
    office_place = _request_param_post(request, 'office_place')
    office_landmark = _request_param_post(request, 'office_landmark')
    office_area = _request_param_post(request, 'office_area')
    office_zip = _request_param_post(request, 'office_zip')
    from users.forms import AccountForm
    accountform = AccountForm({'mobile':mobile,'password':password,
                               'home_place':userprofile.source.place,'home_landmark':userprofile.source.landmark,'home_area':userprofile.source.area,'home_zip':userprofile.source.zip,
                               'office_place':office_place,'office_landmark':office_landmark,'office_area':office_area,'office_zip':office_zip})
    if not accountform.is_valid():
        _add_errormsg(request, 'Please valid information in all the required fields')
        return response(account_template,locals(),request)
    password = accountform.cleaned_data.get('password')
    print 'password:%s' % password
    userprofile.set_password(password)
    print 'password reset done'
    mobile = accountform.cleaned_data.get('mobile')
    userprofile.mobile = mobile
    userprofile.save()
    office_place = accountform.cleaned_data.get('office_place')
    office_landmark = accountform.cleaned_data.get('office_landmark')
    office_area = accountform.cleaned_data.get('office_area')
    office_zip = accountform.cleaned_data.get('office_zip')
    userprofile.set_destination_address(destination_place=office_place,destination_area=office_area,destination_landmark=office_landmark,destination_zip=office_zip)
    _add_successmsg(request, 'Account Information saved Successfully')
    return response(account_template,locals(),request)

def _process_messfood_account_information(userprofile,request,account_template):
    #FIXME:for now this is no different from restfood_account_information saving. Later this will be messfood service specific
    return _process_restfood_account_information(userprofile,request,account_template)
    
def view_save_todaysfood(request):
    if request.method == 'POST':
        fooditem_name = _request_param_post(request,'today_food')
        from restaurants.models import FoodItem
        fooditem = FoodItem.objects.create_fooditem(name=fooditem_name)
        from users.models import UserHomeFood
        userfood = UserHomeFood.objects.create_userfood(userprofile=request.user.get_profile(),fooditem=fooditem)
        from django.template.defaultfilters import date
        from datetime import datetime
        return HttpResponse('<div id="food_%s_%s_%s">%s at %s</div>' % (fooditem.created_on.day,fooditem.created_on.month,fooditem.created_on.year,fooditem.name,date(fooditem.created_on,"f A jS N Y")))

@should_be_admin    
def view_show_registeredusers(request,userslist_template):
    from users.models import UserProfile
    userprofiles = UserProfile.objects.order_by('-created_on')
    return response(userslist_template,locals(),request)

@login_required
def view_myorders(request,userorders_template):
    selected_maintab = 'myorders'
    userprofile = request.user.get_profile()
    from users.models import UserOrder
    userorders = UserOrder.objects.filter(userprofile=userprofile).order_by('-created_on')
    return response(userorders_template,locals(),request)

@should_be_admin
def view_allorders(request,allorders_template):
    from users.models import UserOrder
    userorders = UserOrder.objects.order_by('-created_on')
    return response(allorders_template,locals(),request)

@login_required
@should_be_admin
def view_orderdetails(request,orderdetails_template):
    order_code = _request_param_get(request,'code')
    order = None
    if order_code:
        from users.models import UserOrder
        try:
            order = UserOrder.objects.get(code=order_code)
            userprofile = order.userprofile
        except UserOrder.DoesNotExist:
            pass
    return response(orderdetails_template,locals(),request)

def view_reset_password(request, passwordreset_template):
    from users.forms import PasswordResetForm
    if request.method == 'POST':
        form = PasswordResetForm(post_data(request))
        if not form.is_valid():
            return response(passwordreset_template,locals(),request)
        email = form.cleaned_data.get('email')
        from users.models import UserProfile
        userprofile = UserProfile.objects.get(email=email)
        new_password = userprofile.reset_password()
        from utils.emailer import passwordreset_mailer
        passwordreset_mailer(userprofile, new_password)
        from users.messages import PASSWORD_RESET_EMAIL_SUCCESS
        _add_successmsg(request, PASSWORD_RESET_EMAIL_SUCCESS % email)
        return response(passwordreset_template,locals(),request)
    form = PasswordResetForm()
    return response(passwordreset_template,locals(),request)