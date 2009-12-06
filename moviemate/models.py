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
        user_id = models.IntegerField(unique=True)
        is_admin = models.IntegerField(null=True, db_column='isAdmin', blank=True) # Field name made lowercase.
        is_active = models.IntegerField(null=True, db_column='isActive', blank=True)
        login = models.CharField(max_length=255, primary_key=True)
        psword = models.CharField(max_length=255, blank=True)
        name = models.CharField(max_length=255, blank=True)
        age = models.IntegerField(null=True, blank=True)
        country = models.CharField(max_length=255, blank=True)
        state = models.CharField(max_length=255, blank=True)
        city = models.CharField(max_length=255, blank=True)
        gender = models.CharField(max_length=3, blank=True)
        school = models.CharField(max_length=255, blank=True)
        fantasybudget = models.FloatField(null=True, db_column='fantasyBudget', blank=True) # Field name made lowercase.
        class Meta:
                db_table = u'Users'

        def __unicode__(self):
                return u"%s, <%s>" % (self.name, self.login)

        def get_absolute_url(self):
            return "/users/%s/" % urllib.quote(smart_str(self.username))

        def is_anonymous(self):
            "Always returns False. This is a way of comparing User objects to anonymous users."
            return False

        def is_authenticated(self):
            """Always return True. This is a way to tell if the user has been authenticated in templates.
            """
            return True

        def set_password(self, raw_password):
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.psword = '%s$%s$%s' % (algo, salt, hsh)

        def check_password(self, raw_password):
            """
            Returns a boolean of whether the raw_password was correct. Handles
            encryption formats behind the scenes.
            """
            # Backwards-compatibility check. Older passwords won't include the
            # algorithm or salt.
            if '$' not in self.psword:
                is_correct = (self.psword == get_hexdigest('md5', '', raw_password))
                if is_correct:
                    # Convert the password to the new, more secure format.
                    self.set_psword(raw_password)
                    self.save()
                return is_correct
            return check_password(raw_password, self.psword)

            def set_unusable_password(self):
                # Sets a value that will never be a valid hash
                self.psword = UNUSABLE_PASSWORD

            def has_usable_password(self):
                return self.psword != UNUSABLE_PASSWORD

            def is_admin(self):
                return self.is_admin
            
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

                # Admins have all permissions.
                if self.is_admin:
                    return True
                return False

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