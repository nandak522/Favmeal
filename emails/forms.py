from django import forms
from utils.formfields import CommaSeperatedEmailField

class PasswordResetEmailConversationForm(forms.Form):
    from_email = forms.EmailField(required=True, label='From', initial='(E.g.contact@favmeal.com)',widget=forms.TextInput({'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    to = CommaSeperatedEmailField(required=True, label='To',initial='Seperate Multiple Emails with Commas',widget=forms.TextInput({'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    subject = forms.CharField(max_length=75,required=True,label='Subject',widget=forms.TextInput({'size': 20,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
    description = forms.CharField(max_length=5000,required=True,label='Mail Body',widget=forms.Textarea({'rows':5,'cols':30,'onFocus':'javascript:this.select();','style':'font-size:95%;font-family:sans-serif;color:#555;'}))
