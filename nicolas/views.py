from nicolas.shortcuts import template_response, json_response, html_response

def index(request):
    response = {}
    return template_response('index.html', response, request)

def resume(request):
    response = {}
    return template_response('resume.html', response, request)

def links(request):
    response = {}
    return template_response('links.html', response, request)

def contact(request):
    response = {}
    return template_response('contact.html', response, request)

