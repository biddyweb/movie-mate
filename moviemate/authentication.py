from moviemate.models import Users
from django.conf import settings
from django.forms.fields import email_re
from django.contrib.auth import models as authmodels

class AuthenticationBackend:
	def authenticate(self, username=None, password=None, admin_req=None):
		try:
			user = Users.objects.get(login=username)
			if password == user.psword:
				user.is_active = True
				user.is_superuser = user.isadmin
				user.is_staff = user.isadmin
				user.id = user.user_id
				
				return user
		except Users.DoesNotExist:
			return None
    
	def get_user(self, user_id):
		try:
			return Users.objects.get(pk=user_id)
		except Users.DoesNotExist:
			return None