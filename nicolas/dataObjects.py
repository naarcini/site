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

    def Dictify(self):
        return {'x': self.x, 'y': self.y}

class MetaData(object):
    """
    Stores metadata about project"
    """
    def __init__(self):
        self.length = 650
        self.width = 650
        self.units = "dm"
        self.origin = Coordinate(325, 325)

    def Dictify(self):
        return {'length': self.length, 'width': self.width, 'units': self.units, 'origin': self.origin.Dictify()}

# Robot related

class RobotObject(object):
    """
    Object for a robot
    """
    def __init__(self, identity):
        self.identity = identity
        self.position = Coordinate(-1, -1)
        self.target = Coordinate(-1, -1)
        self.waypoints = []

    def Update(self, position, target, waypoints):
        self.position = position
        self.target = target
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
        self.state = CellState.unexplored
        self.coordinate = Coordinate(-1, -1)

    def Update(self, cellState, coordinate):
        self.state = cellState
        self.coordinate = coordinate

    def Dictify(self):
        return {'state': self.state, 'coordinate': self.coordinate.Dictify()}
    
