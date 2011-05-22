from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden,HttpResponsePermanentRedirect
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.core import urlresolvers
from django.utils.http import urlquote

class Message:
    def __init__(self):
        self.remindermessages=[]
        self.errormessages=[]
        self.informativemessages=[]

    def add_reminder_msg(self, message):
        if message not in self.remindermessages:
            self.remindermessages.append(message)
            
    def add_error_msg(self, message):
        if message not in self.errormessages:
            self.errormessages.append(message)
            
    def add_msg(self, message):
        if message not in self.informativemessages:
            self.informativemessages.append(message)
            
    def explode(self):
        return {"remindermessages":self.remindermessages, 
                "errormessages":self.errormessages, 
                "informativemessages":self.informativemessages}

class MessagesMiddleware(object):
    def process_request(self, request):
        request.fmessages = Message()