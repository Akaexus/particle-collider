from modules.simulation.area import Area
from modules.simulation.particle import Particle
import secrets
import pyglet
import math

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

    def distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    def unit_to_pixel(self, e):
        return e * self.pixels_per_unit

    def coordinate_to_pixel(self, c):
        return self.unit_to_pixel(c) + self.offset

    def unit_pos_to_pixel(self, p):
        return list(map(lambda e: self.coordinate_to_pixel(e), p))


    def draw(self, window):
        # początkowe wyliczenia pixeli
        self.area_height = window.height * 0.9
        self.offset = window.height * 0.05
        self.area_width = self.config.area['width'] / self.config.area['height'] * self.area_height
        self.pixels_per_unit = self.area_height / self.config.area['height']

        batch = pyglet.graphics.Batch()
        rectangle = pyglet.shapes.Rectangle(
            x=self.offset,
            y=self.offset,
            width=self.area_width,
            height=self.area_height,
            color=(255, 255, 255),
            batch=batch
        )

        circles = []
        lines = []
        for particle in self.area.particles:
            # linia wskazująca kierunek wektora prędkości
            a = particle.vy / particle.vx
            b = particle.y - a * particle.x
            candidate_points = []
            if particle.vx < 0:  # leci w lewo
                # lewa sciana
                candidate_points.append([
                    0,  # x
                    b  # y
                ])
            elif 0 < particle.vx:  # leci w prawo
                candidate_points.append([
                    self.config.area['width'],
                    a * self.config.area['width'] + b
                ])

            if particle.vy < 0:  # leci w dół
                # dolna sciana
                candidate_points.append([
                    -b / a,  # x
                    0
                ])
            elif 0 < particle.vy:  # leci w góre
                candidate_points.append([
                    (self.config.area['height'] - b) / a,
                    self.config.area['height']
                ])

            if len(candidate_points):
                candidate_points.sort(key=lambda p: self.distance([particle.x, particle.y], p))
                second_point = candidate_points[0]

                lines.append(pyglet.shapes.Line(
                    self.coordinate_to_pixel(particle.x),
                    self.coordinate_to_pixel(particle.y),
                    self.coordinate_to_pixel(second_point[0]),
                    self.coordinate_to_pixel(second_point[1]),
                    width=max(self.unit_to_pixel(self.config.atoms['radius'])*0.25, 1),
                    color=particle.color,
                    batch=batch
                ))

            circles.append(pyglet.shapes.Circle(
                x=self.coordinate_to_pixel(particle.x),
                y=self.coordinate_to_pixel(particle.y),
                radius=max(self.unit_to_pixel(self.config.atoms['radius']), 1),
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