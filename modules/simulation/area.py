class Area:
    particles = []
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def addParticle(self, particle):
        self.particles.append(particle)