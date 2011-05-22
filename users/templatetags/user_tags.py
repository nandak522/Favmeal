from django import template
from django.template import resolve_variable, NodeList
from django.contrib.auth.models import Group
register = template.Library()

@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins %} ... {% else %} ... {% endifusergroup %}

    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires 1 argument.")
    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifusergroup',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return GroupCheckNode(group, nodelist_true, nodelist_false)

class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
    def render(self, context):
        user = resolve_variable('user', context)
        if not user or not user.is_authenticated():
            return self.nodelist_false.render(context)
        try:
            group = Group.objects.get(name=self.group)
        except Group.DoesNotExist:
            return self.nodelist_false.render(context)
        if group in user.groups.all():
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

def render_login_profile(user):
    if user.is_authenticated():
        return {'logged_in':True,'user':user}
    from users.forms import LoginForm
    return {'logged_in':False,'login_form':LoginForm(),'user':user}
register.inclusion_tag('users/templatetags/render_login_profile.html')(render_login_profile)

def messages(context):
    return context.get('request').fmessages.explode()
register.inclusion_tag("users/templatetags/render_messages.html", takes_context=True)(messages)

def renderoldfood(user):
    from users.models import UserHomeFood
    return {'userfoods':UserHomeFood.objects.filter(userprofile=user.get_profile())}
register.inclusion_tag('users/templatetags/render_oldfood.html')(renderoldfood)

def _get_route_for_user(user):
    try:
        userprofile = user.get_profile()
        source_area = userprofile.source.area
        from tracks.models import Halt
        source_area_halt = Halt.objects.get(name=source_area)
        destination_area = userprofile.destination.area
        destination_area_halt = Halt.objects.get(name=destination_area)
        from tracks.models import Route
        for route in Route.objects.all():
            route_halts = route.halts.all()
            if source_area_halt in route_halts and destination_area_halt in route_halts:
                return route,source_area_halt.position_wrt_route(route)
        return None
    except Exception:
        from tracks.models import Route
        return Route.objects.get(code='R001'),13

def rendermap(user,restaurant=None):
    userprofile = user.get_profile()
    route,route_plotting_start_postion = _get_route_for_user(user)
    ########### for safety ################
    from tracks.models import Route
    routes = Route.objects.all()
    #######################################
    return {'user':user, 'route':route,'route_plotting_start_postion':route_plotting_start_postion,'routes':routes}
#    source_latitude = userprofile.source.latitude
#    source_longitude = userprofile.source.longitude
#    if not restaurant:
#        if userprofile.get_service_type() == 'homefood':
#            destination_latitude = userprofile.destination.latitude
#            destination_longitude = userprofile.destination.longitude
#            return {'user':user,'source_latitude':source_latitude, 'source_longitude':source_longitude, 'destination_latitude':destination_latitude, 'destination_longitude':destination_longitude}
#        return {'user':user,'source_latitude':source_latitude, 'source_longitude':source_longitude, 'destination_latitude':None, 'destination_longitude':None}
#    destination_latitude = restaurant.address.latitude
#    destination_longitude = restaurant.address.longitude
#    return {'user':user,'source_latitude':source_latitude, 'source_longitude':source_longitude, 'destination_latitude':destination_latitude, 'destination_longitude':destination_longitude}
register.inclusion_tag('users/templatetags/render_map.html')(rendermap)

def renderlocationmarker(user, location_type):
    return {'location_type':location_type}
register.inclusion_tag('users/templatetags/render_locationmarker.html')(renderlocationmarker)