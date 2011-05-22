from django import template
register = template.Library()

def renderorderedmenuitems(items_string):
    items = []
    if items_string:
        menuitems_ids = [str(item) for item in items_string.split(',')]
    menuitems_ids_by_quantity = _clean_menuitems_by_quantity(menuitems_ids)
    menuitems_by_quantity_dicts = []
    from restaurants.models import RestaurantMenuItem
    for menuitem_id in menuitems_ids_by_quantity.keys():
        menuitems_by_quantity_dicts.append({'item':RestaurantMenuItem.objects.get(id=menuitem_id), 'quantity':menuitems_ids_by_quantity[menuitem_id]})
    return {'items':menuitems_by_quantity_dicts}
register.inclusion_tag('restaurants/templatetags/render_ordered_menuitem.html')(renderorderedmenuitems)

def _clean_menuitems_by_quantity(menuitem_ids):
    cleaned_menuitems = {}
    for item_id in menuitem_ids:
        if cleaned_menuitems.has_key(item_id):
            cleaned_menuitems[item_id]+=1
        else:
            cleaned_menuitems[item_id]=1
    return cleaned_menuitems