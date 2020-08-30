class Particle:
    x = 0
    y = 0
    vx = 0
    vy = 0
    id = 0
    def __init__(self, position, velocity, color):
        [self.x, self.y] = position
        [self.vx, self.vy] = velocity
        self.color = color
        self.id = Particle.id
        Particle.id+=1


    def __repr__(self):
        return '#{} [{:.2f}x, {:.2f}y] @ {:.2f}, {:.2f}'.format(self.id, self.x, self.y, self.vx, self.vy)