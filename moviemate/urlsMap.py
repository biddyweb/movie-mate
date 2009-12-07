from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response

from moviemate import models

#USER SITE functions
def root_view(request):
    return HttpResponseRedirect('/home/')

def home(request):
	#movie = models.Movie.objects.filter(name="Toy Story")[0]
    	return render_to_response('index.html', locals())
