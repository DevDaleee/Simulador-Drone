import math

class Drone:
    def __init__(self, did, x, y, dest_x, dest_y, speed):
        self.id            = did
        self.x             = float(x)
        self.y             = float(y)
        self.dest_x        = float(dest_x)
        self.dest_y        = float(dest_y)
        self.speed         = speed
        self.status        = "em_voo"
        self.dist_traveled = 0.0
        self.start_step    = 0
        self.end_step      = None

    def move(self, step):
        if self.status != "em_voo":
            return

        direcao_x = self.dest_x - self.x
        direcao_y = self.dest_y - self.y

        dist = math.sqrt(direcao_x**2 + direcao_y**2)

        if dist <= self.speed:
            self.dist_traveled += dist
            self.x, self.y     = self.dest_x, self.dest_y
            self.status        = "chegou"
            self.end_step      = step
        else:
            self.x             += (direcao_x / dist) * self.speed
            self.y             += (direcao_y / dist) * self.speed
            self.dist_traveled += self.speed
