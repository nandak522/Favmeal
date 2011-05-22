from django import template
register = template.Library()

def renderallroutes():
    from tracks.models import Route
    routes = Route.objects.all()
    return {'routes':routes}
register.inclusion_tag('tracks/templatetags/render_allroutes.html')(renderallroutes)