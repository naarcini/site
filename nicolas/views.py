from nicolas.shortcuts import template_response, json_response, html_response
from nicolas.dataObjects import Coordinate, MetaData, RobotObject, CellState, Cell
from nicolas.serverFunctions import ClearRobot, ResetMap, CheckMap, ResetInstruction, ResetDb, GetRobotId, JsonToRobot, JsonToCellArray, JsonToInstruction, UpdateRobot, UpdateMap, UpdateInstruction, DrawMap
from nicolas.models import Robot, Map, Waypoint

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
    response = {}
    return template_response('robotapp.html', response, request)

def instruction(request):
    """
    Usage:
        Lightweight call to be used frequently by robot

    GET:
        Gets stored instruction for specified robot
    POST:
        Update instruction for specified robot
    DELETE:
        Resets stored instruction for specified robot
    """
    robotId = GetRobotId(request.GET)

    if robotId is None:
        response = \
        {
            'status': 'error',
            'details': 'all requests must have a robot ID',
        }

    elif request.method == "GET":
        # Access instruction from DB
        response = {}

    elif request.method == "POST":
        # Update robot instruction
        response = {}

    elif request.method == "DELETE":
        # Wipe instructions for this robot
        response = {}

    else:
        response = \
        {
            'status': 'error',
            'details': 'Must use GET or DELETE',
        }

    return json_response(response)

def robot(request):
    """
    Usage:
        Generic call to be used by server and robot

    GET:
        Gets all data for specified robot
    POST:
        Create or update robot data
    DELETE:
        Wipes all data for specified robot
    """
    robotId = GetRobotId(request.GET)

    if request.method == "POST":
        # Get or update robot data in DB
        response = {}

    elif robotId is None:
        response = \
        {
            'status': 'error',
            'details': 'GET or DELETE requests must have a robot ID',
        }

    elif request.method == "GET":
        # Access robot from DB
        response = {}

    elif request.method == "DELETE":
        # Wipe all robot related data
        response = {}

    else:
        response = \
        {
            'status': 'error',
            'details': 'Must use GET or DELETE',
        }

    return json_response(response)


def serverMap(request):
    """
    Usage:
        To be used primarily by robot to update map

    GET:
        Gets specified cells and updates PNG file
    POST:
        Update section of map
    DELETE:
        Resets map
    """
    if not CheckMap():
        response = \
        {
            'status': 'error',
            'details': 'Map has not been built yet',
        }

    elif request.method == "GET":
        # Get specified map segments in JSON blob and update PNG file
        mapResult = DrawMap()

        if 'payload' not in request.GET:
            response = \
            {
                'status': 'error',
                'details': 'No data for a specific cell specified',
                'drawStatus': mapResult[0],
                'drawDetails': mapResult[1],
            }
            return json_response(response)

 
        blob = str(request.GET['payload'])
        result = JsonToCellArray(blob)

        if result[0] == 'error':
            response = \
            {
                'status': result[0],
                'details': result[1],
                'drawStatus': mapResult[0],
                'drawDetails': mapResult[1],
            }
            return json_response(response)

        requestCellArray = result[2]
        responseCellArray = []

        for cell in requestCellArray:
            if cell.ValidateCoordinates():
                mapData = Map.objects.get(x = cell.coordinate.x, y = cell.coordinate.y)
                cell.state = mapData.state
                responseCellArray.append(cell)

        response = \
        {
            'status': 'ok',
            'details': [ cell.Dictify() for cell in responseCellArray ],
            'drawStatus': mapResult[0],
            'drawDetails': mapResult[1],
        }

    elif request.method == "POST":
        # Update map bits specified in call
        blob = request.read()
        result = JsonToCellArray(blob)

        if result[0] == 'error':
            response = \
            {
                'status': result[0],
                'details': result[1],
            }
            return json_response(response)

        requestCellArray = result[2]

        for cell in requestCellArray:
            if cell.ValidatePopulated():
                mapData = Map.objects.get(x = cell.coordinate.x, y = cell.coordinate.y)
                mapData.state = cell.state
                mapData.save()

        response = \
        {
            'status': 'ok',
            'details': 'Successfully updated map',
        }

    elif request.method == "DELETE":
        # Reset map in DB
        result = ResetMap()
        reponse = \
        {
            'status': result[0],
            'details': result[1],
        }

    else:
        response = \
        {
            'status': 'error',
            'details': 'Must use GET, POST, or DELETE'
        }

    return json_response(response)

def masterReset(request):
    """
    Usage:
        If something goes wrong or if testing, this could be handy

    DELETE:
        Completely reset db
    """
    if request.method == "DELETE":
        # Delete everything
        result = ResetDb()
        response = \
        {
            'status': result[0],
            'details': result[1],
        }

    else:
        response = \
        {
            'status': 'error',
            'details': 'Must use DELETE. Are you sure you want to do this?',
        }

    return json_response(response)

