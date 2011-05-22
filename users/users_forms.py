from django import forms

service_type_choices = (('regular','regular'),
                        ('ondemand','ondemand')
                        )

class LoginForm(forms.Form):
    lusername = forms.EmailField(required=True, label='Email', initial='(E.g.yourname@yourdomain.com)',widget=forms.TextInput({'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    lpassword = forms.CharField(required=True, label='password', widget=forms.PasswordInput({'size': 20,'style':'font-size:95%;font-weight:bold;color:#555;'}))
    
class ForgotPasswordForm(forms.Form):    
    email = forms.EmailField(required=True, label='Email', help_text='(E.g.myemail@gmail.com,youremail@yahoo.com)')
    
class AccountForm(forms.Form):
    password = forms.CharField(required=False, max_length=120,label='Password',widget=forms.PasswordInput({'size': 20,'style':'font-size:95%;font-weight:bold;color:#555;'}))
    mobile = forms.IntegerField(required=False, label='Mobile', initial='(E.g. 9959959959)',widget=forms.TextInput({'size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_place = forms.CharField(max_length=100,required=True,label='House Number',initial='(E.g. 3-6-511)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_landmark = forms.CharField(max_length=50,required=True,label='Office Landmark',initial='(E.g. Mitra Motors,Gurukul High School)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_area = forms.CharField(max_length=50,required=True,label='Office Area',initial='(E.g. HimayathNagar)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    home_zip = forms.CharField(max_length=6,required=False,label='Zip',initial='(E.g. 500063)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_place = forms.CharField(max_length=100,required=True,label='Office Place',initial='(E.g. 4th Floor, Building No.10,Titus)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_landmark = forms.CharField(max_length=50,required=True,label='Office Landmark',initial='(E.g. Mindspace)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_area = forms.CharField(max_length=50,required=True,label='Office Area',initial='(E.g. Hi-TechCity,Madhapur)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    office_zip = forms.CharField(max_length=6,required=False,label='Zip',initial='(E.g. 500081)',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))

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
        
    def render_homefood_accountform(self):
        from utils import loader
        template = "users/homefood_accountform_template.html"
        return loader.render_to_string(template,{'accountform':self})
        
    def render_restaurantfood_accountform(self):
        from utils import loader
        template = "users/restfood_accountform_template.html"
        return loader.render_to_string(template,{'accountform':self})

    def render_messfood_accountform(self):
        from utils import loader
        template = "users/messfood_accountform_template.html"
        return loader.render_to_string(template,{'accountform':self})

class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True, label='Email', initial='(E.g.yourname@yourdomain.com)',widget=forms.TextInput({'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        from users.models import UserProfile
        try:
            UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError('"%s" is not registered with us. Please enter a valid Email Address' % email)
        return email