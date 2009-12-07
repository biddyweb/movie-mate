from django.conf.urls.defaults import *
from moviemate.settings import APP_PATH

from moviemate import views

from moviemate.urlsMap import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^moviemate/', include('moviemate.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    
    (r'^movie/(?P<mid>\d+)$', views.movie_page),
    (r'^$', root_view),
    (r'^home/$', home),
    
    (r'^person/(?P<pid>\d+)$', views.person_page),
    
    #basic search
    (r'^search/(?P<type>(movie|person|friend))/(?P<query>.+)$', views.basic_search),
    
    url(r'^top5$', views.ajax_top_five, name='demo_ajax_top_five'),
    
    (r'^review/$', views.review),
    
    #to make static files work
    (r'^files/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': APP_PATH + '/templates/'}
    ),

)
