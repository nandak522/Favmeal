from django.contrib.auth.models import User
from django.forms.fields import email_re

class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        print 'Inside EmailBackend'
        print 'username = %s ' % username
        print 'password = %s ' % password
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    print 'EmailBackend authentication done'
                    return user
                print 'authentication not done'
                return None
            except User.DoesNotExist:
                print 'new user'
                return None
            