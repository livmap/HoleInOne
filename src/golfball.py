import math

class GolfBall:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vX = 0
        self.vY = 0
        self.hitVelocity = 0
        self.xRatio = 0
        self.yRatio = 0

    def setHitVelocity(self, hV):
        self.hitVelocity = hV

    def getVelocity(self):
        return math.sqrt(math.pow(self.vX, 2) + math.pow(self.vY, 2))
    