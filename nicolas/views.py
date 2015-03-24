from nicolas.shortcuts import template_response, json_response, html_response
from nicolas.serverFunctions import RobotAction, UserInterfaceAction, MasterResetAction, LocalIpAction, BuildJsonResponse
from nicolas.drawMap import VisualMapAction
from nicolas.models import Robot, Misc
import uuid

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

def comingsoon(request):
    response = {}
    return template_response('comingsoon.html', response, request)

def webapp(request):
    response = {'robotIds': list(Robot.objects.values_list('id', flat=True).order_by('id')), 'ips': list(Misc.objects.values_list('value', flat=True).order_by('id'))}
    return template_response('robotapp.html', response, request)

def robot(request):
    """
    Usage:
        Requests that are specific to the robot

    GET:
        Gets all data for specified robot
    POST:
        Create or update robot data and update cells, if any
    DELETE:
        Wipes all data for specified robot
    """
    try:
        response = RobotAction(request.GET, request.read(), request.method)
    except Exception as ex:
        print 'Error: {0}'.format(str(ex))
        response = BuildJsonResponse(False, 'An unexpected server error occurred: {0}'.format(str(ex)))
    return json_response(response)


def userInterface(request):
    """
    Usage:
        Requests that are specific to the UI

    GET:
        Updates map and gets robot information if specified
    POST:
        Updates instruction to send to robot
    DELETE:
        Resets specified aspect of db
        - "map" resets whole map
        - "waypoints" with robot ID resets waypoints
        - "instruction" with robot ID resets instruction
        - "robot" with robot ID resets entire robot
    """
    try:
        response = UserInterfaceAction(request.GET, request.read(), request.method)
    except Exception as ex:
        print 'Error: {0}'.format(str(ex))
        response = BuildJsonResponse(False, 'An unexpected server error occurred: {0}'.format(str(ex)))
    return json_response(response)

def visualMap(request):
    """
    Usage:
        Regenerate visual map based on db data

    GET:
        Build and save map
    """
    try:
        if 'userId' not in request.session:
            request.session['userId'] = str(uuid.uuid1())
        response = VisualMapAction(request.GET, request.read(), request.method, request.session['userId'])
    except Exception as ex:
        print 'Error: {0}'.format(str(ex))
        response = BuildJsonResponse(False, 'An unexpected server error occurred: {0}'.format(str(ex)))
    return json_response(response)

def visualMapImages(request):
    response = {}
    if 'userId' in request.GET:
        response['userId'] = request.GET['userId']

    return template_response('robotMap.html', response, request)

def masterReset(request):
    """
    Usage:
        If something goes wrong or if testing, this could be handy

    DELETE:
        Completely reset db
    """
    try:
        response = MasterResetAction(request.GET, request.read(), request.method)
    except Exception as ex:
        print 'Error: {0}'.format(str(ex))
        response = BuildJsonResponse(False, 'An unexpected server error occurred {0}'.format(str(ex)))
    return json_response(response)

def localip(request):
    """
    Usage:
        For symposium, just save the IP of the robot

    POST:
        Save this IP for this robot
    """
    try:
        response = LocalIpAction(request.GET, request.method)
    except Exception as ex:
        print 'Error: {0}'.format(str(ex))
        response = BuildJsonResponse(False, 'An unexpected server error occurred {0}'.format(str(ex)))
    return json_response(response)

