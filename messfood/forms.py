from django import forms
from messfood.models import Mess
from django.conf import settings

def messes_list():
    existing_messes = [(mess.id, mess.name) for mess in list(Mess.objects.all())]
    existing_messes.append((-1, 'Another Mess'))
    return existing_messes

def messfood_available_destinations():
    available_destinations = settings.SERVICE_AVAILABLE_DESTINATIONS
    available_destinations.append((-1, 'Other'))
    return available_destinations

class MessFoodRegistrationForm(forms.Form):
    remail = forms.EmailField(required=True, label='Email', initial='(E.g. somebody@xyz.com)', widget=forms.TextInput({'tabindex':'1', 'size': 20, 'style':'font-size:95%;font-family:sans-serif;color:#555;', 'onFocus':'javascript:this.select();return false', 'onBlur':'javascript:check_email_exists();'}))
    rpassword = forms.CharField(required=True, max_length=120, label='Password', widget=forms.PasswordInput({'tabindex':'2', 'size': 20, 'style':'font-size:95%;font-weight:bold;color:#555;'}))
    mobile = forms.IntegerField(required=True, label='Mobile', initial='(E.g. 9959959959)', widget=forms.TextInput({'tabindex':'3', 'onFocus':'javascript:this.select();return false', 'size': 20, 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    service_type = forms.CharField(required=True, label='Service', widget=forms.HiddenInput(), initial='messfood')
    mess = forms.ChoiceField(choices=messes_list(), widget=forms.Select({'tabindex':'4', 'onChange':'javascript:showmess();return false;'}), required=True)
    office_place = forms.CharField(max_length=100, required=True, label='Office Place', initial='(E.g. 4th Floor, Building No.10,Titus)', widget=forms.TextInput({'tabindex':'5', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_landmark = forms.CharField(max_length=50, required=True, label='Office Landmark', initial='(E.g. Mindspace)', widget=forms.TextInput({'tabindex':'6', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_area = forms.ChoiceField(choices=messfood_available_destinations(), required=True, widget=forms.Select({'tabindex':'7', 'style':'font-size:95%;font-family:sans-serif;color:#555;', 'onChange':'javascript:show_other_area();return false;'}))    
    office_other_area = forms.CharField(required=False, label='Other Area', widget=forms.TextInput({'tabindex':'8', 'size': 20, 'style':'font-size:95%;font-family:sans-serif;color:#555;display:none;'}))
    office_city = forms.CharField(max_length=50, required=False, label='City', initial='(E.g. Hyderabad)', widget=forms.TextInput({'tabindex':'9', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_zip = forms.CharField(max_length=6, required=False, label='Zip', initial='(E.g. 500081)', widget=forms.TextInput({'tabindex':'10', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    
    def __init__(self,*args,**kwargs):
        super(MessFoodRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['mess'].choices = messes_list()

    def clean_mess(self):
        mess_id = self.cleaned_data.get('mess')
        if mess_id == '-1':
            raise forms.ValidationError('Please Select a Mess')
        if int(mess_id) not in [mess.id for mess in Mess.objects.all()]:
            raise forms.ValidationError('Please Select a Mess')
        return mess_id
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        str_mobile = str(mobile)
        if len(str_mobile) == 10 and str_mobile.startswith('9'):
            try:
                if int(str_mobile) <= 9999999999:
                    return mobile
            except:
                raise forms.ValidationError('Invalid Mobile Number. Should be 10 digits and must Start with 9')
        else:
            raise forms.ValidationError('Invalid Mobile Number. Should be 10 digits and must Start with 9')
        
    def clean_office_place(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'office_place', 'Invalid Address Information')
    
    def clean_office_landmark(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'office_landmark', 'Invalid Address Information')
    
    def clean_office_area(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'office_area', 'Invalid Address Information')
    
class MessCreationForm(forms.Form):
    mess_place = forms.CharField(max_length=100, required=True, label='Mess Place', initial='(E.g. Ruchira)', widget=forms.TextInput({'tabindex':'11', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    mess_landmark = forms.CharField(max_length=50, required=True, label='Mess Landmark', initial='(E.g. Image Hospitals)', widget=forms.TextInput({'tabindex':'12', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    mess_area = forms.CharField(max_length=50, required=True, label='Mess Area', initial='(E.g. Ravuri Hills)', widget=forms.TextInput({'tabindex':'13', 'size': 20, 'onFocus':'javascript:this.select();return false;', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    mess_city = forms.CharField(max_length=50, required=False, label='City', initial='(E.g. Hyderabad)', widget=forms.TextInput({'tabindex':'14', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    mess_zip = forms.CharField(max_length=6, required=False, label='Zip', initial='(E.g. 500081)', widget=forms.TextInput({'tabindex':'15', 'size': 20, 'onFocus':'javascript:this.select();return false', 'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    
    def clean_mess_place(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'mess_place', 'Invalid Address Information')
    
    def clean_mess_landmark(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'mess_landmark', 'Invalid Address Information')
    
    def clean_mess_area(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self, 'mess_area', 'Invalid Address Information')