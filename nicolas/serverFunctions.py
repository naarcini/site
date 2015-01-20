from nicolas.dataObjects import Coordinate, MetaData, RobotObject, CellState, Cell
from nicolas.models import Robot, Map, Waypoint
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

    try:
        Robot.objects.get(pk = robotId).delete()
    except Robot.DoesNotExist:
        return BuildJsonResponse(False, 'No robot of this id found')
    except Robot.MultipleObjectsReturned:
        return BuildJsonResponse(False, 'Multiple robots of this id found')

    return BuildJsonResponse(True, 'Successfully deleted robot data')

def BuildMap():
    """
    Return full map to initial, unexplored state
    This is SUPER SLOW
    """
    Map.objects.all().delete()

    print "Starting to build map"

    for i in range(-MetaData.origin.x, MetaData.xMax - MetaData.origin.x):
        for j in range(-MetaData.origin.y, MetaData.yMax - MetaData.origin.y):
            cell = Map(x = i, y = j, state = CellState.unexplored)
            cell.save()

    print "Finished building map"

    return BuildJsonResponse(True, 'Successfully regenerated map')

def ResetMap():
    """
    Just reset explored state of existing map
    """
    Map.objects.all().update(state = CellState.unexplored)
    return BuildJsonResponse(True, 'Successfully reset map exploration state')

def ResetInstruction(robotId):
    """
    Clear instruction for a particular robot
    """
    try:
        robot = Robot.objects.get(pk = robotId)
        robot.xTarget = None
        robot.yTarget = None
        robot.xTargetMetric = None
        robot.yTargetMetric = None
        robot.save()
    except Robot.DoesNotExist:
        return BuildJsonResponse(False, 'No robot of this id found')
    except Robot.MultipleObjectsReturned:
        return BuildJsonResponse(False, 'Multiple robots of this id found')

    return BuildJsonResponse(True, 'Successfully cleared instructions')

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

def JsonToRobot(jsonBlob):
    """
    Convert a chunk of json to RobotObject
    """
    return BuildJsonResponse(False, 'Not Implemented')

def JsonToCellArray(jsonBlob):
    """
    Convert a chunk of json to an array of Cell objects
    """
    if jsonBlob is None:
        return BuildJsonResponse(False, 'No JSON detected in body')

    result = []
    try:
        rawData = json.loads(jsonBlob)
    except:
        return BuildJsonResponse(False, 'Bad JSON')

    if 'cells' not in rawData:
        return BuildJsonResponse(False, 'Could not find map data in request')

    for cell in rawData['cells']:
        newCell = Cell() 
        if 'x' in cell:
            newCell.coordinate.x = int(cell['x'])
        if 'y' in cell:
            newCell.coordinate.y = int(cell['y'])
        if 'state' in cell:
            newCell.state = int(cell['state'])
        result.append(newCell)

    response = BuildJsonResponse(True, 'Successfully decoded json to cell array')
    response['result'] = result
    return response

def JsonToInstruction(jsonBlob):
    """
    Convert a chunk of json to an Instruction
    """
    return None

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

# Update DB Functions
# If desired, we can rip out some code from views and put it here instead

def UpdateRobot(robotId, robot, waypoints):
    """
    Update specified robot in db
    """
    return BuildJsonResponse(False, 'Not Implemented')

def UpdateMap(cellArray):
    """
    Update cells in map corresponding to input
    """
    return BuildJsonResponse(False, 'Not Implemented')

def UpdateInstruction(robotId, coordinate):
    """
    Update the instruction for one robot
    """
    return BuildJsonResponse(False, 'Not Implemented')

# Map Drawing Functions

def DrawMap():
    """
    Use DB to draw out map and robots to 3 PNG files of sizes
    650x650, 1300x1300, and 2600x2600 (layer1, layer2, layer3)
    """
    return BuildJsonResponse(False, 'Not Implemented')

 
