from modules.simulation.area import Area
from modules.simulation.particle import Particle
from modules.simulation.detector import Detector
import secrets
import pyglet
import math


class Engine:
    counter = 0
    collision_lock = []

    def __init__(self, config):
        self.config = config
        self.ticks_left = self.config.simulation_time
        self.area = Area(height=config.area['height'], width=config.area['width'])
        rand = secrets.SystemRandom()
        self.area.particles = []
        for i in range(config.atoms['number']):
            x = rand.random() * (config.area['width'] - config.atoms['radius'] * 2) + config.atoms['radius']
            y = rand.random() * (config.area['height'] - config.atoms['radius'] * 2) + config.atoms['radius']
            vx = rand.random() * config.atoms['max_velocity'] * 2 - config.atoms['max_velocity']
            vy = rand.random() * config.atoms['max_velocity'] * 2 - config.atoms['max_velocity']

            self.area.addParticle(Particle([x, y], [vx, vy], self.random_color(rand)))

        # collision_lock
        for i in range(self.config.atoms['number']):
            self.collision_lock.append([])
            for j in range(self.config.atoms['number']):
                self.collision_lock[i].append(False)
        # detektor
        self.detector = Detector(self.config)

    def random_color(self, rand):
        max_color = 250
        return rand.randint(0, max_color), rand.randint(0, max_color), rand.randint(0, max_color)

    def tick(self):
        index = 0

        for particle in self.area.particles:
            # v * t = s
            particle.x += particle.vx * self.config.tick_time
            # s = v *t + 0.5*a*t^2
            particle.y += particle.vy * self.config.tick_time + -self.config.gravity * 0.5 * (self.config.tick_time**2)
            particle.vy += -self.config.gravity * self.config.tick_time  # zmiana prędkości pionowej wynikająca z grawitacji

            # kolizje
            # sciany
            if particle.vy < 0 and particle.y - self.config.atoms['radius'] - self.config.collision_tolerance <= 0:  # dolna
                particle.vy = -particle.vy
            elif particle.vy > 0 and particle.y + self.config.atoms['radius'] + self.config.collision_tolerance >= self.config.area['height']:  # gorna
                particle.vy = -particle.vy

            if particle.vx < 0 and particle.x - self.config.atoms['radius'] - self.config.collision_tolerance <= 0: # lewa
                particle.vx = -particle.vx
            elif particle.vx > 0 and particle.x + self.config.atoms['radius'] + self.config.collision_tolerance >= self.config.area['width']:  # prawa
                if self.config.detector['position'] <= particle.y <= self.config.detector['position'] + self.config.detector['height']:
                    self.detector.emit(particle, self.config.simulation_time - self.ticks_left)
                particle.vx = -particle.vx
            # inne atomy
            for index2, particle2 in enumerate(self.area.particles):
                if 0 < self.distance([particle.x, particle.y], [particle2.x, particle2.y]) <= (2 * self.config.atoms['radius'] + self.config.collision_tolerance):
                    if not (self.collision_lock[index][index2] and self.collision_lock[index2][index]):
                        self.collision_lock[index][index2] = True
                        self.collision_lock[index2][index] = True

                        # okreslamy prosta miedzy środkami atomów
                        collision_axis_a = (particle2.y - particle.y) / (particle2.x - particle.x)
                        collision_axis_b = particle2.y - collision_axis_a * particle2.x
                        reversed_collision_axis_a = -1 / collision_axis_a
                        # particle2
                        # okreslamy prostą prostopadłą do osi zderzenia, ale przechodzącą przez punkt na
                        # który wskazuje wektor prędkości
                        velocity_point_x = particle2.x + particle2.vx
                        velocity_point_y = particle2.y + particle2.vy
                        reversed_collision_axis_b = velocity_point_y - reversed_collision_axis_a * velocity_point_x
                        particle2_collision_parallel_velocity_vector_point_x = (reversed_collision_axis_b - collision_axis_b) / (collision_axis_a - reversed_collision_axis_a)
                        particle2_collision_parallel_velocity_vector_point_y = particle2_collision_parallel_velocity_vector_point_x *  reversed_collision_axis_a + reversed_collision_axis_b
                        p2_vector_vx = particle2_collision_parallel_velocity_vector_point_x - particle2.x
                        p2_vector_vy = particle2_collision_parallel_velocity_vector_point_y - particle2.y

                        velocity_point_x = particle.x + particle.vx
                        velocity_point_y = particle.y + particle.vy
                        reversed_collision_axis_b = velocity_point_y - reversed_collision_axis_a * velocity_point_x
                        particle_collision_parallel_velocity_vector_point_x = (reversed_collision_axis_b - collision_axis_b) / (collision_axis_a - reversed_collision_axis_a)
                        particle_collision_parallel_velocity_vector_point_y = particle_collision_parallel_velocity_vector_point_x *  reversed_collision_axis_a + reversed_collision_axis_b
                        p1_vector_vx = particle_collision_parallel_velocity_vector_point_x - particle.x
                        p1_vector_vy = particle_collision_parallel_velocity_vector_point_y - particle.y

                        particle.vx -= p1_vector_vx
                        particle.vy -= p1_vector_vy
                        particle.vx += p2_vector_vx
                        particle.vy += p2_vector_vy

                        particle2.vx -= p2_vector_vx
                        particle2.vy -= p2_vector_vy
                        particle2.vx += p1_vector_vx
                        particle2.vy += p1_vector_vy
                else:
                    # print(self.ticks_left)
                    # print(self.config.atoms['number'], len(self.area.particles))
                    self.collision_lock[index][index2] = False
                    self.collision_lock[index2][index] = False
            index += 1
            

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
        detector = pyglet.shapes.Rectangle(
            x=self.offset + self.area_width,
            y=self.offset + self.unit_to_pixel(self.config.detector['position']),
            width=max(1, self.area_width*0.02),
            height=self.unit_to_pixel(self.config.detector['height']),
            color=(255, 0, 0),
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
                    color=map(lambda x: x + int((255 - x) * 0.7), particle.color),
                    batch=batch
                ))

            circles.append(pyglet.shapes.Circle(
                x=self.coordinate_to_pixel(particle.x),
                y=self.coordinate_to_pixel(particle.y),
                radius=max(self.unit_to_pixel(self.config.atoms['radius']), 1.25),
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