from django.forms.fields import email_re
from django.forms import CharField

class CommaSeperatedEmailField(CharField):
    def __init__(self,comma_separated_emails):
        self.emails = comma_separated_emails
        
        