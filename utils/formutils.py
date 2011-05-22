import re
from django import forms

address_info_pattern = re.compile(r'^\(E\.g\.[\w\s\-\,\.]+\)$',re.IGNORECASE)

def _clean_address_attribute(form,attribute_name,error_message):
    if not form.cleaned_data.get(attribute_name):
        raise forms.ValidationError('This field is required')
    if re.match(address_info_pattern, form.cleaned_data.get(attribute_name)):
        raise forms.ValidationError(error_message)
    return form.cleaned_data.get(attribute_name)