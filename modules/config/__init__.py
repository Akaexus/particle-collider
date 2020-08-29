# -*- coding: utf-8 -*-
import json
class Config:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        for property in config:
            setattr(self, property, config[property])
        self.tick_time = 1 / (self.time_factor * self.atoms['max_velocity'])
        if len(self.duration):
            self.time_limited = True
            if 'ticks' in self.duration:
                self.ticks_left = self.duration['ticks']
            elif 'units' in self.duration:
                self.ticks_left = int(self.duration['units'] / self.tick_time)
        else:
            self.time_limited = False

    def test(self):
        tests = [
            {
                'test': lambda c: 0 < c.area['height'] >= 20 and 0 < c.area['width'] >= 20,
                'error': 'Rozmiary pudełka są zbyt małe.'
            },
            {
                'test': lambda c: c.area['height'] / c.area['width'] >= 5,
                'error': 'Proporcje pudełka są nieprawidłowe.'
            },
            {
                'test': lambda c: 0 < c.atoms['number'] <= 0.25 * c.area['height'] * c.area['width'],
                'error': 'Liczba atomów nie jest prawidłowa!'
            },
            {
                'test': lambda c: c.time_factor >= min(c.area['height'], c.area['width']),
                'error': 'Parametr czasu jest zbyt niski!'
            }
        ]