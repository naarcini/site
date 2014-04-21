from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    response = {}
    return HttpResponse(render_to_response('nicolas/index.html', response, context_instance=RequestContext(request)))
