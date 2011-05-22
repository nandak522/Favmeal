from django.http import HttpResponse,Http404,HttpResponseRedirect,HttpResponsePermanentRedirect
from utils import response,post_data,_request_param_post,_request_param_get
from utils import login_required,should_be_admin
from django.conf import settings
from django.utils import simplejson

def view_restaurants(request,restaurants_registration_template,restaurants_template):
    selected_maintab = 'restaurantfood'
    if request.user.is_authenticated():
        from restaurants.models import Restaurant
        restaurants = Restaurant.premiumobjects.all().order_by('-created_on')
        return response(restaurants_template,locals(),request)
    else:
        from restaurants.models import Restaurant
        restaurants = Restaurant.premiumobjects.all().order_by('-created_on')
        from restaurants.forms import RestaurantFoodRegistrationForm
        form = RestaurantFoodRegistrationForm()
        return response(restaurants_registration_template,locals(),request)

def view_restaurantmenu(request,ralias,restaurantmenu_template):
    restaurant = _get_restaurant_from_alias(ralias)
    menu = restaurant.menuitems()
    grouped_menu = {}
    for item in menu:
        tags = item.item.tags.all()
        for tag in tags:
            if grouped_menu.has_key(tag.name):
                grouped_menu[tag.name].append(item)
            else:
                grouped_menu.__setitem__(tag.name,[])
    return response(restaurantmenu_template,locals(),request)

def view_orderconfirm(request,ordercofirm_template):
    order_information = []
    restaurant_alias = _request_param_post(request,'ralias')
    from restaurants.models import Restaurant
    restaurant = Restaurant.objects.get(alias=restaurant_alias)
    item_ids = _request_param_post(request,'item_ids').split(',')
    item_ids_quantity = _cleanquantity(item_ids)
    menu_items = []
    from restaurants.models import RestaurantMenuItem
    foodscost = 0
    vat_charges = 0
    for item_id in item_ids_quantity.keys():
        menuitem = RestaurantMenuItem.objects.get(id=item_id)
        foodscost+=item_ids_quantity[item_id]*menuitem.cost
        order_information.append({'menuitem':menuitem, 'quantity':item_ids_quantity[item_id],'netcost':item_ids_quantity[item_id]*menuitem.cost})
    vat_percentage = settings.VAT_PERCENTAGE
    vat_percentage_display = vat_percentage*100
    foodscost = foodscost.__float__()
    vat_charges = foodscost*vat_percentage
    service_charge = settings.RESTAURANTFOOD_SERVICE_CHARE
    total_bill = foodscost+vat_charges+service_charge
    from datetime import datetime,timedelta
    time_now = datetime.now()
    min_time = datetime(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year, hour=settings.DELIVERY_TIMINGS_START_HOUR,minute=0,second=0)
    max_time = datetime(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year, hour=settings.DELIVERY_TIMINGS_END_HOUR,minute=0,second=0)
    hours = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    available_hours = []
    for hour in hours:
        if (time_now+timedelta(hours=hour)) <= max_time:
            available_hours.append(hour)
    if available_hours:
        food_deliverytime = time_now+timedelta(hours=available_hours[0])
    return response(ordercofirm_template,locals(),request)

def view_computedeliverytime(request,deliverytime_template):
    hours = _request_param_post(request,'hours')
    delivery_time = None
    from datetime import datetime,timedelta
    delivery_time = datetime.now()+timedelta(hours=int(hours))
    return response(deliverytime_template,locals(),request)

def view_ordersummary(request,orderdone_template):
    order_code = _request_param_get(request,'code')
    from users.models import UserOrder
    try:
        order = UserOrder.objects.get(code=order_code)
    except UserOrder.DoesNotExist:
        order = None
    return response(orderdone_template,locals(),request)

def view_makeorder(request):
    try:
        response_dict = {}
        totalbill = _request_param_post(request,'totalbill')
        ordered_items = _clean_ordered_items_ids_quantity(_request_param_post(request,'ordered_items_ids_quantity'))
        deliverytime = _clean_time(_request_param_post(request,'deliverytime'))
        userprofile = request.user.get_profile()
        from users.models import UserOrder
        order = UserOrder.objects.create_userorder(userprofile=userprofile, deliverytime=deliverytime, menuitems=ordered_items, totalcost=totalbill)
        response_dict['id'] = order.id
        response_dict['code'] = order.code
        response_dict['status'] = '200'
    except Exception,e:
        from utils.emailer import mail_admins
        mail_admins(e,locals())
        print 'Exception:%s' % e.__str__()
        response_dict['id'] = None
        response_dict['code'] = None
        response_dict['status'] = '500'
    return HttpResponse(simplejson.dumps(response_dict))

@should_be_admin
def view_orderdelete(request):
    order_id = _request_param_get(request,'orderid')
    if order_id:
        from users.models import UserOrder
        try:
            order = UserOrder.objects.get(id=order_id)
        except UserOrder.DoesNotExist:
            return HttpResponse('Order Doesn\'t Exist')
        order.delete()
        return HttpResponse('Order Deleted')
    return HttpResponse('Enter Order')

def _clean_ordered_items_ids_quantity(ordered_items_ids_quantity):
    ordered_items_ids_quantity = ordered_items_ids_quantity.split(',')
    ordered_items = ''
    item_number = 0
    for item_quantity in ordered_items_ids_quantity:
        item_number += 1
        item_id,quantity = item_quantity.split('-')
        for i in range(int(quantity)):
            ordered_items+=item_id
            if i != int(quantity)-1:
                ordered_items+=','
        if item_number != len(ordered_items_ids_quantity):
            ordered_items+=','
    return ordered_items

def _clean_time(string_time):
    if string_time.__contains__(':'):
        hours_minutes = string_time.split(':')
        hours = int(hours_minutes[0])
        minutes,am_pm = hours_minutes[1].split(' ')
        am_pm = str(am_pm).strip()
        minutes = int(minutes)
    else:
        hours_minutes = string_time.split(' ')
        hours = int(hours_minutes[0])
        minutes = 0
        am_pm = str(hours_minutes[1]).strip()
    if am_pm == 'PM':
        hours = 12+int(hours)
    from datetime import datetime
    time_now = datetime.now()
    cleaned_time = datetime(time_now.year,time_now.month,time_now.day,hours,minutes)
    return cleaned_time

############# Helpers #################
def _cleanquantity(item_ids):
    items_quantity = {}
    for item_id in item_ids:
        if items_quantity.has_key(str(item_id[10:])):
            items_quantity['%s' % item_id[10:]]+=1
        else:
            items_quantity['%s' % item_id[10:]]=1
    return items_quantity

def _get_restaurant_from_alias(ralias):    
    from restaurants.models import Restaurant
    try:
        return Restaurant.objects.get(alias=ralias)
    except Restaurant.DoesNotExist:
        raise Http404