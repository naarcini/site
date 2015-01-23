from nicolas.serverFunctions import BuildJsonResponse
from nicolas.models import Map

# Used to draw visual map

def VisualMapAction(params, body, method):
    """
    Use DB to draw out map and robots to 3 PNG files of sizes
    650x650, 1300x1300, and 2600x2600 (layer1, layer2, layer3)
    """
    return BuildJsonResponse(False, 'Not Implemented')
