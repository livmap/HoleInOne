class World:
    def __init__(self, f, ws, wd, r):
        self.friction = f
        self.windSpeed = ws
        self.windDirection = wd
        self.rain = r

        if self.rain:
            self.friction = 0.75 * self.friction
