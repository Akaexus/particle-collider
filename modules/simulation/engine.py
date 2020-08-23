from modules.simulation.area import Area
from modules.simulation.particle import Particle
import secrets
import pyglet

class Engine:
    counter = 0
    def __init__(self, config):
        self.config = config
        self.area = Area(height=config.area['height'], width=config.area['width'])
        rand = secrets.SystemRandom()
        for i in range(config.atoms['number']):
            x = rand.random() * (config.area['width'] - config.atoms['radius'] * 2) + config.atoms['radius']
            y = rand.random() * (config.area['height'] - config.atoms['radius'] * 2) + config.atoms['radius']
            vx = rand.random() * config.area['width'] * 2 - config.area['width']
            vy = rand.random() * config.area['height'] * 2 - config.area['height']

            self.area.addParticle(Particle([x, y], [vx, vy], self.random_color(rand)))

    def random_color(self, rand):
        return (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))


    def tick(self):
        self.counter += 1

    def draw(self, window):
        # początkowe wyliczenia pixeli
        area_height = window.height * 0.9
        offset = window.height * 0.05
        area_width = self.config.area['width'] / self.config.area['height'] * area_height
        pixels_per_unit = area_height / self.config.area['height']

        batch = pyglet.graphics.Batch()
        rectangle = pyglet.shapes.Rectangle(
            x=offset,
            y=offset,
            width=area_width,
            height=area_height,
            color=(255, 255, 255),
            batch=batch
        )
        print(self.config.atoms['radius']*pixels_per_unit)
        circles = []
        for particle in self.area.particles:
            circles.append(pyglet.shapes.Circle(
                x=offset + (pixels_per_unit * particle.x),
                y=offset + (pixels_per_unit * particle.y),
                radius=pixels_per_unit * self.config.atoms['radius'],
                color=particle.color,
                batch=batch
            ))

        # circle = pyglet.shapes.Circle(x=100, y=150, radius=100, color=(50, 225, 30), batch=batch)
        batch.draw()
        # label = pyglet.text.Label(str(self.counter),
        #                           font_name='Times New Roman',
        #                           font_size=36,
        #                           x=window.width // 2, y=window.height // 2,
        #                           anchor_x='center', anchor_y='center')
        # label.draw()