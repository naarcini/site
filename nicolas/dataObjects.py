# General
def enum(**enums):
    return type('Enum', (), enums)

class Coordinate(object):
    """
    Stores a generic coordinate
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Update(self, x, y):
        self.x = x
        self.y = y

    def ValidateExists(self):
        return (self.x is not None and self.y is not None
            and self.x in range(-MetaData.origin.x, MetaData.xMax - MetaData.origin.x)
            and self.y in range (-MetaData.origin.y, MetaData.yMax - MetaData.origin.y))

    def Dictify(self):
        return [self.x, self.y]

class MetaData(object):
    """
    Stores metadata about project"
    """
    xMax = 650
    yMax = 650
    units = "dm"
    origin = Coordinate(325, 325)
    init = False

    def __init__(self):
        self.init = True

    def Dictify(self):
        return {'xMax': self.xMax, 'yMax': self.yMax, 'units': self.units, 'origin': self.origin.Dictify()}

# Robot related

class RobotObject(object):
    """
    Object for a robot
    """
    def __init__(self, robotId):
        self.robotId = robotId
        self.position = Coordinate(None, None)
        self.exactPosition = Coordinate(None, None)
        self.instruction = Coordinate(None, None)
        self.waypoints = []

    def PositionExists(self):
        return self.position.ValidateExists()

    def ExactPositionExists(self):
        return self.exactPosition.ValidateExists()

    def InstructionExists(self):
        return self.instruction.ValidateExists()

    def WaypointsExist(self):
        return (self.waypoints is not None and isinstance(self.waypoints, list) and len(self.waypoints) > 0)

    def Dictify(self):
        response = {'robotId': self.robotId}

        if self.PositionExists():
            response['position'] = self.position.Dictify()
        if self.ExactPositionExists():
            response['exactPosition'] = self.exactPosition.Dictify()
        if self.InstructionExists():
            response['instruction'] = self.instruction.Dictify()
        if self.WaypointsExist():
            response['waypoints'] = self.waypoints

        return response

# Map related

CellState = enum(unexplored = 0, empty = 1, blocked = 2)

class Cell(object):
    """
    Stores state of each individual cell in grid
    """
    def __init__(self):
        self.state = None
        self.coordinate = Coordinate(None, None)

    def ValidateCoordinates(self):
        return self.coordinate.ValidateExists()

    def ValidatePopulated(self):
        return (self.ValidateCoordinates() and self.state is not None and self.state in range(0, 3))

    def Dictify(self):
        if self.state is None:
            return [self.coordinate.x, self.coordinate.y]
        else:
            return [self.coordinate.x, self.coordinate.y, self.state]
    
