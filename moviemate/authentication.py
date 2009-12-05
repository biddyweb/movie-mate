from moviemate.models import Users
from django.conf import settings
from django.forms.fields import email_re

class AuthenticationBackend:
    def authenticate(self, username=None, password=None, admin_req=None):
        if email_re.search(username):
            try:
                user = Users.objects.get(login=username)
                return user
            except Users.DoesNotExist:
                return None
    
    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None