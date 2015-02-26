from nicolas.dataObjects import Coordinate, MetaData, RobotObject, CellState, Cell
from nicolas.models import Robot, Map, Waypoint
from ast import literal_eval
import json

# Reset Functions

def ClearRobot(robotId):
    """
    Remove specified robot from db, including associated waypoints
    If none specified, remove all robots
    """
    if robotId is None:
        Waypoint.objects.all().delete()
        Robot.objects.all().delete()
        return BuildJsonResponse(True, 'Successfully deleted all robots and waypoints')

    Waypoint.objects.filter(robotId = robotId).delete()

    result = GetSpecificRobot(robotId)
    if not IsOperationSuccess(result):
        return result

    result['robot'].delete()
    return BuildJsonResponse(True, 'Successfully deleted robot data')

def ResetInstruction(robotId):
    """
    Clear instruction for a particular robot
    """
    result = GetSpecificRobot(robotId)
    if not IsOperationSuccess(result):
        return result

    robot = result['robot']
    robot.xTarget = None
    robot.yTarget = None
    robot.save()

    return BuildJsonResponse(True, 'Successfully cleared instructions')

def ResetWaypoints(robotId, isReal):
    """
    Clear waypoints for a particular robot
    """
    if robotId is None:
        return BuildJsonResponse(False, 'Null robot ID')

    Waypoint.objects.filter(robotId = robotId, realWaypoint = isReal).delete()
    return BuildJsonResponse(True, 'Successfully deleted waypoints')

def BuildMap():
    """
    Return full map to initial, unexplored state
    This is SUPER SLOW
    """
    Map.objects.all().delete()

    print "Starting to build map"

    cellList = []
    for i in reversed(range(-MetaData.origin.y, MetaData.yMax - MetaData.origin.y)):
        for j in range(-MetaData.origin.x, MetaData.xMax - MetaData.origin.x):
            cellList.append(Map(x = j, y = i, state = CellState.unexplored))

    Map.objects.bulk_create(cellList)
    print "Finished building map"

    return BuildJsonResponse(True, 'Successfully regenerated map')

def ResetMap():
    """
    Just reset explored state of existing map
    """
    Map.objects.all().update(state = CellState.unexplored)
    return BuildJsonResponse(True, 'Successfully reset map exploration state')

def CheckMap():
    """
    If map is not populated, say so
    """
    if Map.objects.all().count() < (MetaData.xMax * MetaData.yMax):
        return False

    return True

def ResetDb():
    """
    Master Reset of DB
    """
    result = ClearRobot(None)
    if not IsOperationSuccess(result):
        return result

    if CheckMap():
        result = ResetMap()
    else:
        result = BuildMap()

    if not IsOperationSuccess(result):
        return result

    return BuildJsonResponse(True, 'Successfully reset DB')

# Parse Input functinos

def GetRobotId(args):
    """
    Get the robot ID, if any
    """
    if 'robotId' in args:
        return int(args['robotId'])

    return None

def TextToJson(text):
    """
    Parse some text into json with error checking
    """
    if not text:
        return BuildJsonResponse(False, 'No JSON detected')

    try:
        rawData = json.loads(text)
    except Exception as ex:
        return BuildJsonResponse(False, 'Bad JSON: {0}'.format(str(ex)))

    response = BuildJsonResponse(True, 'Successfully decoded JSON')
    response['rawData'] = rawData
    return response

def ParseRobotRequest(robotId, body):
    """
    Parse some JSON for robot updates
    """
    result = TextToJson(body)
    if not IsOperationSuccess(result):
        return result

    rawData = result['rawData']
    robotUpdates = {}

    if 'cells' in rawData and len(rawData['cells']) > 0:
        result = MapListToCellArray(rawData['cells'])
        if not IsOperationSuccess(result):
            return result

        robotUpdates['cells'] = result['cells']

    if 'robot' in rawData:
        robot = RobotObject(robotId)
        inRobot = rawData['robot']

        if 'position' in inRobot and len(inRobot['position']) > 0:
            result = MapListToCellArray(inRobot['position'])
            if not IsOperationSuccess(result):
                return result

            position = result['cells'][0]
            robot.position.x = position.coordinate.x
            robot.position.y = position.coordinate.y

        if 'exactPosition' in inRobot and len(inRobot['exactPosition']) > 0:
            result = MapListToCellArray(inRobot['exactPosition'])
            if not IsOperationSuccess(result):
                return result

            exactPosition = result['cells'][0]
            robot.exactPosition.x = exactPosition.coordinate.x
            robot.exactPosition.y = exactPosition.coordinate.y

        if 'waypoints' in inRobot and len(inRobot['waypoints']) > 0:
            result = MapListToCellArray(inRobot['waypoints'])
            if not IsOperationSuccess(result):
                return result

            robot.waypoints = [ cell.Dictify() for cell in result['cells'] ]

        robotUpdates['robot'] = robot

    if 'robot' not in robotUpdates and 'cells' not in robotUpdates:
        return BuildJsonResponse(False, 'Unable to parse any input data')

    response = BuildJsonResponse(True, 'Successfully parsed input data')
    response['result'] = robotUpdates
    return response

def BuildJsonResponse(succeeded, message):
    """
    Build a standard response json where "succeeded" is a boolean and "message" contains the details
    """
    response = \
    {
        'status': 'ok' if succeeded else 'error',
        'details': message,
    }
    return response

def IsOperationSuccess(operationResponse):
    """
    Just a convenient and DRY way to check the status of a response
    """
    if 'status' not in operationResponse:
        raise Exception('No status found in a response')
    elif operationResponse['status'] == 'ok':
        return True
    elif operationResponse['status'] == 'error':
        return False
    else:
        raise Exception('Status message not defined')

# Utility Functions

def MapRobotDBToRobotObj(robotDB, waypoints):
    """
    Map a robot model object to a separate object for easier validation/printing
    """
    robot = RobotObject(robotDB.pk)

    robot.position.x = robotDB.xPos
    robot.position.y = robotDB.yPos
    robot.exactPosition.x = robotDB.xExactPos
    robot.exactPosition.y = robotDB.yExactPos
    robot.instruction.x = robotDB.xTarget
    robot.instruction.y = robotDB.yTarget

    if waypoints is not None:
        robot.waypoints = [ [point.x, point.y] for point in waypoints ]

    return robot

def MapListToCellArray(ary):
    """
    Map a list of numbers to an array of cells
    """
    if not isinstance(ary, list):
        return BuildJsonResponse(False, 'Bad list of map cells')

    cells = []
    if not isinstance(ary[0], list):
        newCell = Cell()
        newCell.coordinate.x = int(ary[0])
        newCell.coordinate.y = int(ary[1])
        if len(ary) > 2:
            newCell.state = int(ary[2])
        cells.append(newCell)

    else:
        for cell in ary:
            newCell = Cell()
            newCell.coordinate.x = int(cell[0])
            newCell.coordinate.y = int(cell[1])
            if len(cell) > 2:
                newCell.state = int(cell[2])
            cells.append(newCell)

    response = BuildJsonResponse(True, 'Successfully built cell array')
    response['cells'] = cells
    return response

# DB Functions
# If desired, we can rip out some code from views and put it here instead

def GetSpecificRobot(robotId):
    """
    Gets a specific robot, checking if it exists
    """
    if robotId is None:
        return BuildJsonResponse(False, 'Null robot ID')

    try:
        robot = Robot.objects.get(pk = robotId)
    except Robot.DoesNotExist:
        return BuildJsonResponse(False, 'No robot of this id found')
    except Robot.MultipleObjectsReturned:
        return BuildJsonResponse(False, 'Multiple robots of this id found')

    response = BuildJsonResponse(True, 'Successfully found robot')
    response['robot'] = robot
    return response

def UpdateWaypoints(robotId, waypoints):
    """
    Update specified robot's waypoints
    """
    if robotId is None:
        return BuildJsonResponse(False, 'No robot ID detected')

    if not isinstance(waypoints, list):
        return BuildJsonResponse(False, 'Waypoints must be formatted as a list')

    for waypoint in waypoints:
        if not isinstance(waypoint, list) or not len(waypoint) == 2:
            return BuildJsonResponse(False, 'Waypoints must be formatted as [xPos, yPos]')

    Waypoint.objects.filter(robotId = robotId, realWaypoint = False).delete()
    result = GetSpecificRobot(robotId)
    if not IsOperationSuccess(result):
        return result

    for waypoint in waypoints:
        newWaypoint = Waypoint(robotId = result['robot'], realWaypoint = False, x = int(waypoint[0]), y = int(waypoint[1]))
        newWaypoint.save()
    
    return BuildJsonResponse(True, 'Saved waypoints successfully')

# Robot Endpoint

def RobotAction(params, body, method):
    """
    Performs actions required by robot
    """
    robotId = GetRobotId(params)

    if method == "POST":
        # Parse input
        result = ParseRobotRequest(robotId, body)
        if not IsOperationSuccess(result):
            return result

        robotRequest = result['result']

        # Update cells in map if specified
        if 'cells' in robotRequest:
            if not CheckMap():
                return BuildJsonResponse(False, 'Map has not been built yet')

            for cell in robotRequest['cells']:
                if cell.ValidatePopulated():
                    mapData = Map.objects.get(x = cell.coordinate.x, y = cell.coordinate.y)
                    mapData.state = cell.state
                    mapData.save()

        # Create or update robot data in DB if specified
        if 'robot' in robotRequest:
            robotUpdates = robotRequest['robot']
            if robotId is not None:
                result = GetSpecificRobot(robotId)
                if not IsOperationSuccess(result):
                    return result

                robotDB = result['robot']
                if robotUpdates.PositionExists():
                    robotDB.xPos = robotUpdates.position.x
                    robotDB.yPos = robotUpdates.position.y
                if robotUpdates.ExactPositionExists():
                    robotDB.xExactPos = robotUpdates.exactPosition.x
                    robotDB.yExactPos = robotUpdates.exactPosition.y
                    newWaypoint = Waypoint(robotId = robotDB, realWaypoint = True, x = robotUpdates.exactPosition.x, y = robotUpdates.exactPosition.y)
                    newWaypoint.save()
                robotDB.save()

            elif not robotUpdates.PositionExists() or not robotUpdates.ExactPositionExists():
                    return BuildJsonResponse(False, 'On creation, a robot must have an estimated position and exact position')
            else:
                robotDB = Robot(xPos = robotUpdates.position.x,
                                yPos = robotUpdates.position.y,
                                xExactPos = robotUpdates.exactPosition.x,
                                yExactPos = robotUpdates.exactPosition.y)
                robotDB.save()
                newWaypoint = Waypoint(robotId = robotDB, realWaypoint = True, x = robotUpdates.exactPosition.x, y = robotUpdates.exactPosition.y)
                newWaypoint.save()
                
            robotId = robotDB.pk

            if robotUpdates.WaypointsExist():
                result = UpdateWaypoints(robotId, robotUpdates.waypoints)
                if not IsOperationSuccess(result):
                    result['robotId'] = robotId
                    return result

        # Create a response message
        response = BuildJsonResponse(True, 'Successfully updated database')
        if 'robot' in robotRequest:
            response['robotId'] = robotId

    elif robotId is None:
        response = BuildJsonResponse(False, 'GET or DELETE requests must have a robot ID')

    elif method == "GET":
        # Access robot from DB
        result = GetSpecificRobot(robotId)
        if not IsOperationSuccess(result):
            return result

        waypoints = Waypoint.objects.filter(robotId = robotId, realWaypoint = False)
        robot = MapRobotDBToRobotObj(result['robot'], waypoints)
        response = BuildJsonResponse(True, 'Successfully got robot data')
        response['robot'] = robot.Dictify()

    elif method == "DELETE":
        # Wipe all robot related data
        response = ClearRobot(robotId)

    else:
        response = BuildJsonResponse(False, 'Must use GET, POST, or DELETE')

    return response

# User Interface Endpoint

def UserInterfaceAction(params, body, method):
    """
    Performs actions required by user interface
    """
    if method == "GET":
        # Get the list of robots
        robotIds = list(Robot.objects.values_list('id', flat=True).order_by('id'))
        cells = None
        realWaypoints = None

        # Check for cells to get
        if 'cells' in params:
            if not CheckMap():
                return BuildJsonResponse(False, 'Map has not been built yet')

            result = TextToJson(params['cells'])
            if not IsOperationSuccess(result):
                return result

            result = MapListToCellArray(result['rawData'])
            if not IsOperationSuccess(result):
                return result

            cells = result['cells']
            for cell in cells:
                if cell.ValidateCoordinates():
                    mapData = Map.objects.get(x = cell.coordinate.x, y = cell.coordinate.y)
                    cell.state = mapData.state

        robotId = GetRobotId(params)
        if robotId is not None:
            realWaypoints = Waypoint.objects.filter(robotId = robotId, realWaypoint = True)

        response = BuildJsonResponse(True, 'Successfully acquired data')
        response['robots'] = robotIds
        if cells is not None:
            response['cells'] = [ cell.Dictify() for cell in cells]
        if realWaypoints is not None and len(realWaypoints) > 0:
            response['realWaypoints'] = [ [waypoint.x, waypoint.y] for waypoint in realWaypoints ]

    elif method == "POST":
        # Update Instruction for one robot
        if not body:
            return BuildJsonResponse(False, 'Must include a request body in a POST')

        robotId = GetRobotId(params)
        if robotId is None:
            return BuildJsonResponse(False, 'Must specify a robot ID')

        result = TextToJson(body)
        if not IsOperationSuccess(result):
            return result

        rawData = result['rawData']
        if 'instruction' not in rawData:
            return BuildJsonResponse(False, 'Must include instruction in update')

        result = MapListToCellArray(rawData['instruction'])
        if not IsOperationSuccess(result):
            return result

        instruction = result['cells'][0]
        if not instruction.ValidateCoordinates():
            return BuildJsonResponse(False, 'Invalid instruction coordinates')

        result = GetSpecificRobot(robotId)
        if not IsOperationSuccess(result):
            return result

        robot = result['robot']
        robot.xTarget = instruction.coordinate.x
        robot.yTarget = instruction.coordinate.y
        robot.save()

        response = BuildJsonResponse(True, 'Successfully updated instruction')

    elif method == "DELETE":
        # Find action to perform
        result = TextToJson(body)
        if not IsOperationSuccess(result):
            return result

        rawData = result['rawData']
        if 'data' not in rawData:
            return BuildJsonResponse(False, 'Must specify what sort of thing to delete')

        robotId = GetRobotId(params)
        if rawData['data'] == 'map':
            response = ResetMap()
        elif rawData['data'] == 'waypoints':
            response = ResetWaypoints(robotId, False)
        elif rawData['data'] == 'realWaypoints':
            response = ResetWaypoints(robotId, True)
        elif rawData['data'] == 'instruction':
            response = ResetInstruction(robotId)
        elif rawData['data'] == 'robot':
            if robotId is None:
                response = BuildJsonResponse(False, 'No robot ID included')
            else:
                response = ClearRobot(robotId)
        else:
            response = BuildJsonResponse(False, 'Must specify map, waypoints, instruction, or robot')

    else:
        response = BuildJsonResponse(False, 'Must use GET, POST, or DELETE')

    return response

# Master Reset Endpoint

def MasterResetAction(params, body, method):
    """
    Performs actions required by master reset
    """
    if method == "DELETE":
        # Delete everything
        response = ResetDb()

    else:
        response = BuildJsonResponse(False, 'Must use DELETE. Are you sure you want to do this?')

    return response

