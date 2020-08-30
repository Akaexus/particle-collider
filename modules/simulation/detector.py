class Detector:
    hits = 0
    def __init__(self, config):
        self.config = config
        self.momentums = []
        self.lastTick = 0

    def emit(self, particle, timestamp):
        if self.config.detector['detection_delay'] < timestamp:
            momentum = self.config.atoms['mass'] * 2 * particle.vx
            self.momentums.append(momentum)
            self.lastTick = timestamp

    def getPressure(self):
        time_elapsed = (self.lastTick - self.config.detector['detection_delay']) * self.config.tick_time
        if time_elapsed <= 0:
            return 0
        force = sum(self.momentums) / time_elapsed
        pressure = force / self.config.detector['height']
        return pressure

