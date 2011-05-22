from django.db.models.fields import CharField

class CustomMenuItemsField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 100)
        CharField.__init__(self, *args, **kwargs)
