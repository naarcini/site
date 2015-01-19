from nicolas.dataObjects import Coordinate, MetaData, RobotObject, CellState, Cell
from nicolas.models import Robot, Map, Waypoint

# Reset Functions

def ClearRobot(robotId):
    """
    Remove specified robot from db, including associated waypoints
    If none specified, remove all robots
    """
    return("error", "Not Implemented")

def ResetMap():
    """
    Return full map to initial, unexplored state
    """
    return ("error", "Not Implemented")

def ResetInstruction(robotId):
    """
    Clear instruction for a particular robot
    """
    return ("error", "Not Implemented")

def ResetDb():
    """
    Master Reset of DB
    """
    status = ClearRobots(None)

    if status[0] == "error":
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
    return None

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
    return ("error", "Not Implemented")

def UpdateMap(cellArray):
    """
    Update cells in map corresponding to input
    """
    return ("error", "Not Implemented")

def UpdateInstruction(robotId, coordinate):
    """
    Update the instruction for one robot
    """
    return ("error", "Not Implemented")

# Map Drawing Functions

def DrawMap():
    """
    Use DB to draw out map and robots to 3 PNG files of sizes
    650x650, 1300x1300, and 2600x2600 (layer1, layer2, layer3)
    """
    return("error", "Not Implemented")

 
