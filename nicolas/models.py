from django.db import models

class Robot(models.Model):
    """
    One entry per robot
    """
    xPos = models.IntegerField()
    yPos = models.IntegerField()
    xExactPos = models.IntegerField()
    yExactPos = models.IntegerField()
    xTarget = models.IntegerField(null = True)
    yTarget = models.IntegerField(null = True)

    def __unicode__(self):
        return "robotId: {robotId}; x: {xPos}; y: {yPos}; xExact: {xExactPos}; yExact: {yExactPos}; xTarget: {xTarget}; yTarget: {yTarget}" \
                .format(robotId = self.pk, xPos = self.xPos, yPos = self.yPos, xExactPos = self.xExactPos, yExactPos = self.yExactPos, xTarget = self.xTarget, yTarget = self.yTarget)

class Map(models.Model):
    """
    Stores the entire map
    """
    x = models.IntegerField()
    y = models.IntegerField()
    state = models.IntegerField()

    def __unicode__(self):
        return "x: {x}; y: {y}; state: {state}" \
                .format(x = self.x, y = self.x, state = self.state)

class Waypoint(models.Model):
    """
    Stores the array of waypoints associated with a robot
    """
    robotId = models.ForeignKey(Robot)
    realWaypoint = models.BooleanField(default = False)
    x = models.IntegerField()
    y = models.IntegerField()

    def __unicode__(self):
        return "robotId: {robotId}; x: {x}; y: {y}" \
                .format(robotId = self.robotId, x = self.x, y = self.y)
