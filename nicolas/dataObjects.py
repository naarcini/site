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
        return (self.x is not None and self.y is not None)

    def Dictify(self):
        return {'x': self.x, 'y': self.y}

class MetaData(object):
    """
    Stores metadata about project"
    """
    def __init__(self):
        self.xMax = 650
        self.yMax = 650
        self.units = "dm"
        self.origin = Coordinate(325, 325)

    def Dictify(self):
        return {'xMax': self.xMax, 'yMax': self.yMax, 'units': self.units, 'origin': self.origin.Dictify()}

# Robot related

class RobotObject(object):
    """
    Object for a robot
    """
    def __init__(self, identity):
        self.identity = identity
        self.position = Coordinate(None, None)
        self.positionMetric = Coordinate(None, None)
        self.target = Coordinate(None, None)
        self.targetMetric = Coordinate(None, None)
        self.waypoints = []

    def Update(self, position, positionMetric, target, targetMetric, waypoints):
        self.position = position
        self.positionMetric = positionMetric
        self.target = target
        self.targetMetric = targetMetric
        self.waypoints = waypoints

    def Dictify(self):
        return {'id': self.identity, 'position': self.position.Dictify(), 'target': self.target.Dictify()}

# Map related

CellState = enum(unexplored = 0, empty = 1, blocked = 2)

class Cell(object):
    """
    Stores state of each individual cell in grid
    """
    def __init__(self):
        self.state = None
        self.coordinate = Coordinate(None, None)

    def Update(self, cellState, coordinate):
        self.state = cellState
        self.coordinate = coordinate

    def ValidateCoordinates(self):
        return (
                self.coordinate.ValidateExists()
            and self.coordinate.x in range(-MetaData.origin.x, MetaData.xMax - MetaData.origin.x)
            and self.coordinate.y in range (-MetaData.origin.y, MetaData.yMax - MetaData.origin.y)
            )

    def ValidatePopulated(self):
        return (self.ValidateCoordinates() and self.state is not None)


    def Dictify(self):
        return {'state': self.state, 'x': self.coordinate.x, 'y': self.coordinate.y}
    
