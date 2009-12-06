from moviemate.models import Users
from django.forms.fields import email_re

class AuthenticationBackend:
	def authenticate(self, username=None, password=None, admin_req=None):
		try:
			user = Users.objects.get(email = username)
			#if password == user.psword:
			#	user.id = user.user_id
			return user
		except Users.DoesNotExist:
			return None
    
	def get_user(self, user_id):
		try:
			return Users.objects.get(pk=user_id)
		except Users.DoesNotExist:
			return None