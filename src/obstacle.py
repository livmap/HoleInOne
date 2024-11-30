class Obstacle:
    def __init__(self, x, y, w=None, h=None):
        self.x = x
        self.y = y
        self.w = None
        self.h = None
        if w == None and h != None:
            self.h = h
            ratio = self.h / 500
            self.w = 266 * ratio
        elif w != None and h == None:
            self.w = w
            ratio = self.w / 266
            self.h = 500 * ratio

        
        