from django import forms
from django.conf import settings

def homefood_available_destinations():
    available_destinations = settings.SERVICE_AVAILABLE_DESTINATIONS
    available_destinations.append((- 1, 'Other'))
    return available_destinations

class HomeFoodRegistrationForm(forms.Form):
    remail = forms.EmailField(required=True, label='Email', initial='(E.g. somebody@xyz.com)',widget=forms.TextInput({'tabindex':'1','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;','onFocus':'javascript:this.select();return false;','onBlur':'javascript:check_email_exists();return false;'}))
    rpassword = forms.CharField(required=True, max_length=120,label='Password',widget=forms.PasswordInput({'tabindex':'2','size': 20,'style':'font-size:95%;font-weight:bold;color:#555;'}))
    mobile = forms.IntegerField(required=True, label='Mobile', initial='(E.g. 9959959959)',widget=forms.TextInput({'tabindex':'3','onFocus':'javascript:this.select();return false;','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    service_type = forms.CharField(required=True,label='Service',widget=forms.HiddenInput(),initial='homefood')
    home_place = forms.CharField(max_length=100,required=True,label='House Number',initial='(E.g. 3-6-511)',widget=forms.TextInput({'tabindex':'4','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_landmark = forms.CharField(max_length=50,required=True,label='Office Landmark',initial='(E.g. Mitra Motors,Gurukul High School)',widget=forms.TextInput({'tabindex':'5','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_area = forms.CharField(max_length=50,required=True,label='Office Area',initial='(E.g. HimayathNagar)',widget=forms.TextInput({'tabindex':'6','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_city = forms.CharField(max_length=50,required=False,label='City',initial='(E.g. Hyderabad)',widget=forms.TextInput({'tabindex':'7','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_zip = forms.CharField(max_length=6,required=False,label='Zip',initial='(E.g. 500063)',widget=forms.TextInput({'tabindex':'8','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_place = forms.CharField(max_length=100,required=True,label='Office Place',initial='(E.g. 4th Floor, Building No.10,Titus)',widget=forms.TextInput({'tabindex':'9','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_landmark = forms.CharField(max_length=50,required=True,label='Office Landmark',initial='(E.g. Mindspace)',widget=forms.TextInput({'tabindex':'10','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_area = forms.ChoiceField(choices=homefood_available_destinations(),required=True,widget=forms.Select({'tabindex':'11','style':'font-size:95%;font-family:sans-serif;color:#555;','onChange':'javascript:show_other_area();return false;'}))    
    office_other_area = forms.CharField(required=False, label='Other Area', widget=forms.TextInput({'tabindex':'8', 'size': 20, 'style':'font-size:95%;font-family:sans-serif;color:#555;display:none;'}))
    office_city = forms.CharField(max_length=50,required=False,label='City',initial='(E.g. Hyderabad)',widget=forms.TextInput({'tabindex':'12','size': 20,'onFocus':'javascript:this.select();return false;','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_zip = forms.CharField(max_length=6,required=False,label='Zip',initial='(E.g. 500081)',widget=forms.TextInput({'tabindex':'13','size': 20,'onFocus':'javascript:this.select();return false','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    
    def clean_home_place(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'home_place', 'Invalid Address Information')
    
    def clean_home_landmark(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'home_landmark', 'Invalid Address Information')
    
    def clean_home_area(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'home_area', 'Invalid Address Information')
    
    def clean_office_place(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'office_place', 'Invalid Address Information')
    
    def clean_office_landmark(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'office_landmark', 'Invalid Address Information')
    
    def clean_office_area(self):
        from utils.formutils import _clean_address_attribute
        return _clean_address_attribute(self,'office_area', 'Invalid Address Information')
    
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
    
    def _clean_zip(self,zip_attribute_name):
        zip = self.cleaned_data.get(zip_attribute_name)
        if not zip:
            raise forms.ValidationError('Invalid Zip Code. Please Ensure its a 6 digits number')
        if not len(zip) == 6:
            raise forms.ValidationError('Invalid Zip Code. Please Ensure its a 6 digits number')
        try:
            zip = int(zip)
        except:
            raise forms.ValidationError('Invalid Zip Code. Please Ensure its a 6 digits number')
        return zip 
    
    def clean_home_zip(self):
        return self._clean_zip('home_zip') 
    
    def clean_office_zip(self):
        return self._clean_zip('office_zip') 
