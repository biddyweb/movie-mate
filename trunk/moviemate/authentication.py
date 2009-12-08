from moviemate.models import Users as MyUser
from django.forms.fields import email_re
from moviemate import settings
from django.contrib.auth.backends import ModelBackend

from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model


class AuthenticationBackend(ModelBackend):
	def authenticate(self, username=None, password=None):
		try:
			user = MyUser.objects.get(username=username)
			if user.password == password:
				return user
		except MyUser.DoesNotExist:
			return None
			

			
			
    
	def get_user(self, user_id):
		try:
			return MyUser.objects.get(pk=user_id)
		except MyUser.DoesNotExist:
			return None
			
	@property
	def user_class(self):
		if not hasattr(self, '_user_class'):
			self._user_class = get_model('Users')
			if not self._user_class:
				raise ImproperlyConfigured('Could not get custom user model')
			return self._user_class