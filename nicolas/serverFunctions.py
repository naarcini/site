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
        return('ok', 'Successfully deleted all robots and waypoints')

    Waypoint.objects.filter(robotId = robotId).delete()

    try:
        Robot.objects.get(pk = robotId).delete()
    except Robot.DoesNotExist:
        return('error', 'No robot of this id found')
    except Robot.MultipleObjectsReturned:
        return('error', 'Multiple robots of this id found')

    return('ok', 'Successfully deleted robot data')

def ResetMap():
    """
    Return full map to initial, unexplored state
    """
    Map.objects.all().delete()

    for i in range(-MetaData.orign.x, MetaData.xMax - MetaData.origin.x):
        for j in range(-MetaData.origin.y, MetaData.yMax - MetaData.origin.y):
            cell = Map(x = i, y = j, state = CellState.unexplored)
            cell.save()

    return ('ok', 'Successfully regenerated map')

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
        return('error', 'No robot of this id found')
     except Robot.MultipleObjectsReturned:
        return('error', 'Multiple robots of this id found')

    return ('ok', 'Successfully cleared instructions')

def CheckMap():
    """
    If map is not populated, populate it
    """
    mapData = Map.objects.filter(x = 0, y = 0)

    if len(mapData) == 0:
        ResetMap()

def ResetDb():
    """
    Master Reset of DB
    """
    status = ClearRobot(None)

    if status[0] == 'error':
        return status

    status = ResetMap()
    return status

# Parse Input functinos

def GetRobotId(args):
    """
    Get the robot ID, if any
    """
    if 'robotId' in args:
        return args['robotId']

    return None

def JsonToRobot(jsonBlob):
    """
    Convert a chunk of json to RobotObject
    """
    return None

def JsonToCellArray(jsonBlob):
    """
    Convert a chunk of json to an array of Cell objects
    """
    result = []
    rawData = json.loads(jsonBlob)

    if 'cells' not in rawData:
        return('error', 'Could not find map data in request')

    for cell in rawData['cells']:
        newCell = Cell() 
        if 'x' in cell:
            newCell.coordinate.x = int(cell['x'])
        if 'y' in cell:
            newCell.coordinate.y = int(cell['y'])
        if 'state' in cell:
            newCell.state = int(cell['state'])
        result.append(newCell)

    return('ok', 'Successfully decoded json to cell array', result)
            

def JsonToInstruction(jsonBlob):
    """
    Convert a chunk of json to an Instruction
    """
    return None

# Update DB Functions

def UpdateRobot(robotId, robot, waypoints):
    """
    Update specified robot in db
    """
    return ('error', 'Not Implemented')

def UpdateMap(cellArray):
    """
    Update cells in map corresponding to input
    """
    return ('error', 'Not Implemented')

def UpdateInstruction(robotId, coordinate):
    """
    Update the instruction for one robot
    """
    return ('error', 'Not Implemented')

# Map Drawing Functions

def DrawMap():
    """
    Use DB to draw out map and robots to 3 PNG files of sizes
    650x650, 1300x1300, and 2600x2600 (layer1, layer2, layer3)
    """
    return('error', 'Not Implemented')

 
