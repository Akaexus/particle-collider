# -*- coding: utf-8 -*-
import json
class Config:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        for property in config:
            setattr(self, property, config[property])

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
            }
        ]