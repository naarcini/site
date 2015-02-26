from nicolas.serverFunctions import BuildJsonResponse, IsOperationSuccess, GetRobotId, GetSpecificRobot, MapRobotDBToRobotObj
from nicolas.dataObjects import MetaData, CellState
from nicolas.models import Map, Waypoint
from nicolas.settings import FILE_ROOT
from PIL import Image
import array
import os
import re
import time

# Map colours
UNEXPLORED_RGB = (0x88,0x88,0x88)
EMPTY_RGB = (0xff,0xff,0xff)
BLOCKED_RGB = (0x00,0x00,0x00)

# Robot related colours
TARGET_RGB = (0x33,0x33,0xff)
ROBOT_EXACT_RGB = (0xcc,0x00,0x00)
ROBOT_ESTIMATED_RGB = (0xff,0xb2,0x66)
WAYPOINT_RGB = (0x99,0x00,0x99)
WAYPOINT_REAL_RGB = (0x00,0xcc,0x00)

# Other constants. Must scale by an integer factor
PROFILING = True
NUM_LAYERS = 4
SCALE_FACTOR = int(2)
CHANNELS = 3
FILE_PATH = os.path.join(FILE_ROOT, 'static/images/layer{layerNum}_{userId}.png')
FILE_BASE = os.path.join(FILE_ROOT, 'static/images/')

def ConvertCoordinates(x, y):
    """
    Convert x and y coordinates in map to a coordinate in an image
    """
    if x is None or y is None:
        raise Exception('x and y must have values')

    xPos = x + MetaData.origin.x
    yPos = MetaData.yMax - (y + MetaData.origin.y)

    return CHANNELS * (yPos * MetaData.xMax + xPos)

def CheckBounds(x, y):
    """
    Check if coordinates are in bounds of map
    """
    if x is None or y is None:
        raise Exception('x and y must have values')

    xPos = x + MetaData.origin.x
    yPos = y + MetaData.origin.y

    return (xPos >= 0 and xPos < MetaData.xMax and yPos >= 0 and yPos < MetaData.yMax)

def PlusSign(x, y):
    """
    Form a plus sign centered on x, y
    """
    if x is None or y is None:
        raise Exception('x and y must have values')

    coordinates = []

    if CheckBounds(x, y + 1):
        coordinates.append(ConvertCoordinates(x, y + 1))

    for i in range(-1, 2):
        if CheckBounds(x + i, y):
            coordinates.append(ConvertCoordinates(x + i, y))

    if CheckBounds(x, y - 1):
        coordinates.append(ConvertCoordinates(x, y - 1))

    return coordinates

def Square(x, y):
    """
    Form a square centered on x, y
    """
    if x is None or y is None:
        raise Exception('x and y must have values')

    coordinates = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if CheckBounds(x + i, y + j):
                coordinates.append(ConvertCoordinates(x + i, y + j))

    return coordinates

def DrawMap(params, userId):
    """
    Use DB to draw out map and robots to 4 PNG files of sizes
    650x650, 1300x1300, 2600x2600, and 5200x5200 (layer1, layer2, layer3, layer4)
    """
    # Create the map array for the base case
    if PROFILING:
        start = time.time()
    image = array.array('B', [0x00 for i in range(0, CHANNELS * MetaData.yMax * MetaData.xMax)])

    idx = 0
    px = 0
    mapDB = array.array('B', Map.objects.order_by('-y', 'x').values_list('state', flat=True))

    if PROFILING:
        end = time.time()
        print 'Time to get list: ' + str(end - start)
        start = time.time()
    for yPos in range(0, MetaData.yMax):
        for xPos in range(0, MetaData.xMax):
            pixel = mapDB[px]
            for i in range(0, CHANNELS):
                if pixel == CellState.unexplored:
                    image[idx] = UNEXPLORED_RGB[i]
                elif pixel == CellState.empty:
                    image[idx] = EMPTY_RGB[i]
                elif pixel == CellState.blocked:
                    image[idx] = BLOCKED_RGB[i]
                else:
                    image[idx] = UNEXPLORED_RGB[i]
                idx += 1
            px += 1

    # Replace pixels for robot position and waypoints
    robotId = GetRobotId(params)
    if robotId is not None:
        result = GetSpecificRobot(robotId)
        if not IsOperationSuccess(result):
            return result

        waypoints = Waypoint.objects.filter(robotId = robotId, realWaypoint = False)
        realWaypoints = Waypoint.objects.filter(robotId = robotId, realWaypoint = True)
        robot = MapRobotDBToRobotObj(result['robot'], waypoints)

        # Waypoints and connecting dots, if any
        if robot.WaypointsExist():
            for waypoint in robot.waypoints:
                shape = Square(waypoint[0], waypoint[1])
                for coord in shape:
                    for i in range(0, CHANNELS):
                        image[coord + i] = WAYPOINT_RGB[i]

            # TODO: Now that the waypoints are drawn, connect the dots (maybe)

        # Real waypoints
        if len(realWaypoints) > 0:
            for realWaypoint in realWaypoints:
                shape = Square(int(realWaypoint.x), int(realWaypoint.y))
                for coord in shape:
                    for i in range(0, CHANNELS):
                        image[coord + i] = WAYPOINT_REAL_RGB[i]

        # Robot target, if any
        if robot.InstructionExists():
            shape = Square(robot.instruction.x, robot.instruction.y)
            for coord in shape:
                for i in range(0, CHANNELS):
                    image[coord + i] = TARGET_RGB[i]

        # Robot estimated position
        shape = PlusSign(robot.position.x, robot.position.y)
        for coord in shape:
            for i in range(0, CHANNELS):
                image[coord + i] = ROBOT_ESTIMATED_RGB[i]

        # Robot exact position
        shape = PlusSign(robot.exactPosition.x, robot.exactPosition.y)
        for coord in shape:
            for i in range(0, CHANNELS):
                image[coord + i] = ROBOT_EXACT_RGB[i]

    if PROFILING:
        end = time.time()
        print 'Time to build image array: ' + str(end - start)
        start = time.time()

    # Draw the map and save as layer1.png
    im = Image.frombuffer('RGB', (MetaData.xMax, MetaData.yMax), image, 'raw', 'RGB', 0, 1)
    im.save(FILE_PATH.format(layerNum = 1, userId = userId))

    if PROFILING:
        end = time.time()
        print 'Layer 1: ' + str(end - start)

    # Create upscaled copies of original map
    width = MetaData.xMax
    height = MetaData.yMax
    layerNum = 2
    while layerNum <= NUM_LAYERS:
        if PROFILING:
            start = time.time()

        width *= SCALE_FACTOR
        height *= SCALE_FACTOR

        out = im.resize((width, height))
        out.save(FILE_PATH.format(layerNum = layerNum, userId = userId))

        if PROFILING:
            end = time.time()
            print 'Layer ' + str(layerNum) + ': ' + str(end - start)

        layerNum += 1

    response = BuildJsonResponse(True, 'Successfully created images')
    response['userId'] = userId
    return response

def DeleteMaps():
    """
    Deletes all existing maps if we want to clear some space on the server
    """
    for f in os.listdir(FILE_BASE):
        if re.match('^layer.+\.png$', f):
            os.remove(os.path.join(FILE_BASE, f))

    return BuildJsonResponse(True, 'Successfully deleted images')

def VisualMapAction(params, body, method, userId):
    """
    Use DB to draw out map and robots to 4 PNG files of sizes
    650x650, 1300x1300, 2600x2600, and 5200x5200 (layer1, layer2, layer3, layer4)
    """
    if method == 'GET':
        return DrawMap(params, userId)

    elif method == 'DELETE':
        return DeleteMaps()

    else:
        return BuildJsonResponse(False, 'Must specify GET or DELETE')
        
