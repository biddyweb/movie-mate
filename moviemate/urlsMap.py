from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response

#USER SITE functions
def root_view(request):
    return HttpResponseRedirect('/home/')

def home(request):
    render_to_response('index.html')
