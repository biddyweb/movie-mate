# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#         * Rearrange models' order
#         * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext_lazy as _

class Advertisement(models.Model):
        ad_id = models.IntegerField(primary_key=True)
        product = models.CharField(unique=True, max_length=255, blank=True)
        imgurl = models.CharField(max_length=255, db_column='imgURL', blank=True) # Field name made lowercase.
        refurl = models.CharField(max_length=255, db_column='refURL', blank=True) # Field name made lowercase.
        country = models.CharField(max_length=120, blank=True)
        state = models.CharField(max_length=60, blank=True)
        city = models.CharField(max_length=120, blank=True)
        numclicks = models.IntegerField(null=True, db_column='numClicks', blank=True) # Field name made lowercase.
        commission = models.FloatField(null=True, blank=True)
        startdate = models.DateField(null=True, db_column='startDate', blank=True) # Field name made lowercase.
        enddate = models.DateField(null=True, db_column='endDate', blank=True) # Field name made lowercase.
        targetage = models.IntegerField(null=True, db_column='targetAge', blank=True) # Field name made lowercase.
        class Meta:
                db_table = u'Advertisement'
	
	def __unicode__(self):
		return u'%s' % self.product


class Advertisor(models.Model):
        adver_id = models.IntegerField(primary_key=True)
        name = models.CharField(unique=True, max_length=150, blank=True)
        address = models.CharField(unique=True, max_length=90, blank=True)
        state = models.CharField(unique=True, max_length=60, blank=True)
        city = models.CharField(unique=True, max_length=120, blank=True)
        country = models.CharField(max_length=120, blank=True)
        zip = models.IntegerField(null=True, blank=True)
        balance = models.FloatField(null=True, blank=True)
        class Meta:
                db_table = u'Advertisor'
		
	def __unicode__(self):
		return u'%s' % self.name

class Fantasymovie(models.Model):
        fmid = models.IntegerField(primary_key=True)
        name = models.CharField(unique=True, max_length=150, blank=True)
        script = models.TextField(blank=True)
        avgrating = models.FloatField(null=True, db_column='avgRating', blank=True) # Field name made lowercase.
        numofratings = models.IntegerField(null=True, db_column='numOfRatings', blank=True) # Field name made lowercase.
        mpaa = models.CharField(max_length=15, db_column='MPAA', blank=True) # Field name made lowercase.
        earnings = models.FloatField(null=True, blank=True)
        total_cost = models.FloatField(null=True, blank=True)
        class Meta:
                db_table = u'FantasyMovie'
		
	def __unicode__(self):
		return u'%s' % self.name

class Genre(models.Model):
        gid = models.IntegerField(primary_key=True)
        genre = models.CharField(unique=True, max_length=60, blank=True)
        class Meta:
                db_table = u'Genre'
		
	def __unicode__(self):
		return u'%s' % self.genre

class Likesgenre(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        genre = models.ForeignKey('Genre', to_field='gid', primary_key=True, db_column='genre')
        class Meta:
                db_table = u'LikesGenre'
		
	def __unicode__(self):
		return u"[%s] likes [%s]" % (self.user_id, self.genre)

class Likesmovie(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        mid = models.ForeignKey('Movie', to_field='mid', primary_key=True, db_column='mid')
        class Meta:
                db_table = u'LikesMovie'
        
        def __unicode__(self):
                return u"[%s] likes [%s]" % (self.user_id, self.mid)


class Likesperson(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        pid = models.ForeignKey('Person', to_field='pid', primary_key=True, db_column='pid')
        class Meta:
                db_table = u'LikesPerson'
		
	def __unicode__(self):
		return u"[%s] likes [%s]" % (self.user_id, self.pid)

class Movie(models.Model):
        mid = models.IntegerField(unique=True)
        name = models.CharField(max_length=255, primary_key=True)
        year = models.CharField(max_length=27, primary_key=True)
        avgrating = models.FloatField(null=True, db_column='avgRating', blank=True) # Field name made lowercase.
        numofratings = models.IntegerField(null=True, db_column='numOfRatings', blank=True) # Field name made lowercase.
        mpaa = models.CharField(max_length=15, db_column='MPAA', blank=True) # Field name made lowercase.
        class Meta:
                db_table = u'Movie'

        def __unicode__(self):
                return u"%s\t%s" % (self.name, self.year)


class Person(models.Model):
        pid = models.IntegerField(unique=True)
        name = models.CharField(max_length=255, primary_key=True)
        age = models.IntegerField(null=True, blank=True)
        gender = models.CharField(max_length=3, primary_key=True)
        class Meta:
                db_table = u'Person'
		
	def __unicode__(self):
		return u'%s' % self.name

class Rates(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        mid = models.ForeignKey('Movie', to_field='mid', primary_key=True, db_column='mid')
        rating = models.IntegerField(null=True, blank=True)
        class Meta:
                db_table = u'Rates'
		
	def __unicode__(self):
		return u'[%s] rated [%s] a [%s]' % (self.user_id, self.mid, self.rating)

class Ratesfmovie(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        fmid = models.ForeignKey('Fantasymovie', to_field='fmid', primary_key=True, db_column='fmid')
        rating = models.IntegerField(null=True, blank=True)
        class Meta:
                db_table = u'RatesFMovie'
		
	def __unicode__(self):
		return u'[%s] rated [%s] a [%s]' % (self.user_id, self.fmid, self.rating)

class Review(models.Model):
	user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
	mid = models.ForeignKey('Movie', to_field='mid', primary_key=True, db_column='mid')
	summary = models.TextField(blank=True)
	timestamp = models.DateTimeField(unique=True, primary_key=True)
	class Meta:
                db_table = u'Review'
		
	def __unicode__(self):
		return u'[%s] reviewed [%s]' % (self.user_id, self.review_id)

class Updates(models.Model):
        up_id = models.IntegerField(primary_key=True)
        entity = models.CharField(unique=True, max_length=60, blank=True)
        action = models.CharField(unique=True, max_length=42, blank=True)
        tmstamp = models.DateTimeField(unique=True)
        class Meta:
                db_table = u'Updates'
		
	def __unicode__(self):
		return u'[%s] performed [%s] on [%s]' % (self.up_id, self.action, self.tmstamp)

class Users(models.Model):
        username = models.CharField(max_length=255, primary_key=True, db_column='login')  
        id = models.IntegerField(unique=True, db_column='user_id')
        email = models.CharField(max_length=255, primary_key=True, db_column='login')
        password = models.CharField(max_length=255, blank=True, db_column='psword')
        is_active = models.IntegerField(null=True, db_column='isActive', blank=True)
        is_staff = models.IntegerField(null=True, db_column='isAdmin', blank=True)
        is_superuser = models.IntegerField(null=True, db_column='isAdmin', blank=True)
        name = models.CharField(max_length=255, blank=True)
        age = models.IntegerField(null=True, blank=True)
        country = models.CharField(max_length=255, blank=True)
        state = models.CharField(max_length=255, blank=True)
        city = models.CharField(max_length=255, blank=True)
        gender = models.CharField(max_length=3, blank=True)
        school = models.CharField(max_length=255, blank=True)
        fantasybudget = models.FloatField(null=True, db_column='fantasyBudget', blank=True) # Field name made lowercase.
        objects = UserManager()
        class Meta:
                db_table = u'Users'
                verbose_name = _('user')
                verbose_name_plural = _('users')

        def __unicode__(self):
                return self.username
            
        def get_absolute_url(self):
            return "/users/%s/" % urllib.quote(smart_str(self.username))

        def is_anonymous(self):
            "Always returns False. This is a way of comparing User objects to anonymous users."
            return False

        def is_authenticated(self):
            """Always return True. This is a way to tell if the user has been authenticated in templates.
            """
            return True

        def get_full_name(self):
            "Returns the first_name plus the last_name, with a space in between."
            full_name = u'%s %s' % (self.first_name, self.last_name)
            return full_name.strip()

        def set_password(self, raw_password):
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.password = '%s$%s$%s' % (algo, salt, hsh)

        def check_password(self, raw_password):
            """
            Returns a boolean of whether the raw_password was correct. Handles
            encryption formats behind the scenes.
            """
            # Backwards-compatibility check. Older passwords won't include the
            # algorithm or salt.
            if '$' not in self.password:
                is_correct = (self.password == get_hexdigest('md5', '', raw_password))
                if is_correct:
                    # Convert the password to the new, more secure format.
                    self.set_password(raw_password)
                    self.save()
                return is_correct
            return check_password(raw_password, self.password)

        def set_unusable_password(self):
            # Sets a value that will never be a valid hash
            self.password = UNUSABLE_PASSWORD

        def has_usable_password(self):
            return self.password != UNUSABLE_PASSWORD

        def get_group_permissions(self):
            """
            Returns a list of permission strings that this user has through
            his/her groups. This method queries all available auth backends.
            """
            permissions = set()
            for backend in auth.get_backends():
                if hasattr(backend, "get_group_permissions"):
                    permissions.update(backend.get_group_permissions(self))
            return permissions

        def get_all_permissions(self):
            permissions = set()
            for backend in auth.get_backends():
                if hasattr(backend, "get_all_permissions"):
                    permissions.update(backend.get_all_permissions(self))
            return permissions

        def has_perm(self, perm):
            """
            Returns True if the user has the specified permission. This method
            queries all available auth backends, but returns immediately if any
            backend returns True. Thus, a user who has permission from a single
            auth backend is assumed to have permission in general.
            """
            # Inactive users have no permissions.
            if not self.is_active:
                return False

            # Superusers have all permissions.
            if self.is_superuser:
                return True

            # Otherwise we need to check the backends.
            for backend in auth.get_backends():
                if hasattr(backend, "has_perm"):
                    if backend.has_perm(self, perm):
                        return True
            return False

        def has_perms(self, perm_list):
            """Returns True if the user has each of the specified permissions."""
            for perm in perm_list:
                if not self.has_perm(perm):
                    return False
            return True

        def has_module_perms(self, app_label):
            """
            Returns True if the user has any permissions in the given app
            label. Uses pretty much the same logic as has_perm, above.
            """
            if not self.is_active:
                return False

            if self.is_superuser:
                return True

            for backend in auth.get_backends():
                if hasattr(backend, "has_module_perms"):
                    if backend.has_module_perms(self, app_label):
                        return True
            return False

        def get_and_delete_messages(self):
            messages = []
            for m in self.message_set.all():
                messages.append(m.message)
                m.delete()
            return messages

        def email_user(self, subject, message, from_email=None):
            "Sends an e-mail to this User."
            from django.core.mail import send_mail
            send_mail(subject, message, from_email, [self.email])

        def get_profile(self):
            """
            Returns site-specific profile for this user. Raises
            SiteProfileNotAvailable if this site does not allow profiles.
            """
            if not hasattr(self, '_profile_cache'):
                from django.conf import settings
                if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                    raise SiteProfileNotAvailable
                try:
                    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
                    model = models.get_model(app_label, model_name)
                    self._profile_cache = model._default_manager.get(user__id__exact=self.id)
                    self._profile_cache.user = self
                except (ImportError, ImproperlyConfigured):
                    raise SiteProfileNotAvailable
            return self._profile_cache

class Choosetype(models.Model):
        fmid = models.ForeignKey('Fantasymovie', to_field='fmid', primary_key=True, db_column='fmid')
        genre = models.ForeignKey('Genre', to_field='gid', primary_key=True, db_column='genre')
        class Meta:
                db_table = u'chooseType'
		
	def __unicode__(self):
		return u'[%s] is [%s]' % (self.fmid, self.genre)

class Createfmovie(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='user_id')
        fmid = models.ForeignKey('Fantasymovie', to_field='fmid', primary_key=True, db_column='fmid')
        tmstamp = models.DateTimeField(unique=True)
        class Meta:
                db_table = u'createFMovie'
		
	def __unicode__(self):
		return u'[%s] created [%s] at [%s]' % (self.user_id, self.fmid, self.tmstamp)

class Hasupdate(models.Model):
        user_id = models.ForeignKey('Users', to_field='user_id', unique=True, db_column='user_id')
        up_id = models.ForeignKey('Updates', to_field='up_id', primary_key=True, db_column='up_id')
        class Meta:
                db_table = u'hasUpdate'
		
	def __unicode__(self):
		return u'[%s] has update [%s]' % (self.user_id, self.up_id)

class Hirescast(models.Model):
        fmid = models.ForeignKey('Fantasymovie', to_field='fmid', primary_key=True, db_column='fmid')
        pid = models.ForeignKey('Person', to_field='pid', primary_key=True, db_column='pid')
        salery = models.FloatField(null=True, blank=True)
        class Meta:
                db_table = u'hiresCast'
		
	def __unicode__(self):
		return u'[%s] hired [%s]' % (self.pid, self.fmid)
		

class Hiresdirect(models.Model):
        fmid = models.ForeignKey('Fantasymovie', to_field='fmid', primary_key=True, db_column='fmid')
        pid = models.ForeignKey('Person', to_field='pid', primary_key=True, db_column='pid')
        salery = models.FloatField(null=True, blank=True)
        class Meta:
                db_table = u'hiresDirect'
		
	def __unicode__(self):
		return u'[%s] hired [%s]' % (self.pid, self.mid)

class Isfriend(models.Model):
        uid1 = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='uid1', related_name='uid1')
        uid2 = models.ForeignKey('Users', to_field='user_id', primary_key=True, db_column='uid2', related_name='uid2')
        class Meta:
                db_table = u'isFriend'
		
	def __unicode__(self):
		return u'[%s] is friends with [%s]' % (self.uid1, self.uid2)

class Isinvolved(models.Model):
        pid = models.ForeignKey('Person', to_field='pid', primary_key=True, db_column='pid')
        mid = models.ForeignKey('Movie', to_field='mid', primary_key=True, db_column='mid')
        role = models.CharField(max_length=24, primary_key=True)
        class Meta:
                db_table = u'isInvolved'
		
	def __unicode__(self):
		return u'[%s] is involved with [%s] as [%s]' % (self.pid, self.mid, self.role)

class Istype(models.Model):
        mid = models.ForeignKey('Movie', to_field='mid', primary_key=True, db_column='mid')
        gid = models.ForeignKey('Genre', to_field='gid', primary_key=True, db_column='gid')
        class Meta:
                db_table = u'isType'
		
	def __unicode__(self):
		return u'[%s] is [%s]' % (self.mid, self.gid)

class Suppliesad(models.Model):
        adver_id = models.ForeignKey('Advertisor', to_field='adver_id', primary_key=True, db_column='adver_id')
        ad_id = models.ForeignKey('Advertisement', to_field='ad_id', primary_key=True, db_column='ad_id')
        class Meta:
                db_table = u'suppliesAd'
		
	def __unicode__(self):
		return u'[%s] advertises [%s]' % (self.adver_id, self.ad_id)

class Targetsgenre(models.Model):
        ad_id = models.ForeignKey('Advertisement', to_field='ad_id', primary_key=True, db_column='ad_id')
        genre = models.ForeignKey('Genre', to_field='gid', primary_key=True, db_column='gid')
        class Meta:
                db_table = u'targetsGenre'
		
	def __unicode__(self):
		return u'[%s] targets [%s]' % (self.ad_id, self.genre)



admin.site.register(Advertisement)
admin.site.register(Advertisor)
admin.site.register(Fantasymovie)
admin.site.register(Genre)
admin.site.register(Likesgenre)
admin.site.register(Likesmovie)
admin.site.register(Likesperson)
admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Rates)
admin.site.register(Ratesfmovie)
admin.site.register(Review)
admin.site.register(Updates)
admin.site.register(Users)
admin.site.register(Choosetype)
admin.site.register(Createfmovie)
admin.site.register(Hasupdate)
admin.site.register(Hirescast)

admin.site.register(Hiresdirect)
admin.site.register(Isfriend)
admin.site.register(Isinvolved)
admin.site.register(Istype)
admin.site.register(Suppliesad)
admin.site.register(Targetsgenre)