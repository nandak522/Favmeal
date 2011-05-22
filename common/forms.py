from django import forms

class ContactUsQueryForm(forms.Form):
    name = forms.CharField(max_length=50,required=False,label='Name',initial='',widget=forms.TextInput({'tabindex':'1','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    email = forms.EmailField(required=True, label='Email', initial='',widget=forms.TextInput({'tabindex':'2','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    query = forms.CharField(max_length=1000,required=True,label='Name',initial='',widget=forms.Textarea({'tabindex':'3','rows': 2,'cols':10,'style':'height:100px;font-size:95%;font:bold 1em sans-serif;color:#555;'}))
    
class ReferFriendForm(forms.Form):
    name = forms.CharField(max_length=50,required=False,label='',initial='',widget=forms.TextInput({'tabindex':'1','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    email = forms.EmailField(required=True, label='', initial='',widget=forms.TextInput({'tabindex':'2','size': 20,'style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    ref_emails = forms.CharField(max_length=1000,required=False,label='',initial='',widget=forms.Textarea({'tabindex':'3','rows': 2,'cols':19,'style':'height:50px;font-size:95%;font-family: sans-serif;color:#555;'}))
    ref_mobiles = forms.CharField(max_length=1000,required=False,label='',initial='',widget=forms.Textarea({'tabindex':'4','rows': 2,'cols':19,'style':'height:50px;font-size:95%;font-family: sans-serif;color:#555;'}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.strip()

    def clean_ref_mobiles(self):
        ref_emails = self.cleaned_data.get('ref_emails')
        ref_mobiles = self.cleaned_data.get('ref_mobiles')
        if not ref_mobiles:
            if not ref_emails:
                raise forms.ValidationError('Either your friends email id(s) or mobile no(s) are required to provide.')
            return ref_mobiles.strip()                     
        list_mobiles = ref_mobiles.strip().lower().split(',')
        if list_mobiles:
            for mobile in list_mobiles:
                if len(mobile) == 10 and mobile.startswith('9'):
                    try:
                        if int(mobile) <= 9999999999:
                            continue
                    except:
                        raise forms.ValidationError('Invalid Mobile Number')
                else:
                    raise forms.ValidationError('Invalid Mobile Number')
        return ref_mobiles.strip()
    
    def clean_ref_emails(self):
        unsuccessful_emails_list, successful_emails_list = [],[]
        email = self.cleaned_data.get('email')
        ref_emails = self.cleaned_data.get('ref_emails')
        ref_mobiles = self.cleaned_data.get('ref_mobiles')
        if not ref_emails:
            if not ref_mobiles:
                raise forms.ValidationError('Either your friends email id(s) or mobile no(s) are required to provide.')                     
            return ref_emails.strip()
        all_emails_list = ref_emails.strip().split(',')
        from django.forms.fields import email_re
        for email_id in all_emails_list:
            if email_re.search(email_id.strip().lower()):
                if email_id == email:
                    if all_emails_list.__len__() == 1:
                        raise forms.ValidationError('You can\'t refer yourself, right!')
                else:
                    successful_emails_list.append(email_id)
            else:
                unsuccessful_emails_list.append(email_id)
        return ",".join(["%s" % (email) for email in successful_emails_list])
    