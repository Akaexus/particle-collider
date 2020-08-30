from modules.config import Config
from modules.simulation.engine import Engine
config = Config()

engine = Engine(config)


import pyglet

window = pyglet.window.Window(resizable=True)
pyglet.gl.glClearColor(0.8, 0.8, 0.8, 0.8)
def update_frames(dt):
    global engine
    global config
    for i in range(config.ticks_per_frame):
        if config.time_limited and engine.ticks_left > 0 or not config.time_limited:
            engine.tick()
            if config.time_limited:
                engine.ticks_left -= 1
        elif config.time_limited and engine.ticks_left <= 0:
            print('Ciśnienie liniowe: {}'.format(engine.detector.getPressure()))
            exit()

@window.event
def on_draw():
    global engine
    window.clear()
    engine.draw(window)
    # label = pyglet.text.Label(str(counter),
    #                           font_name='Times New Roman',
    #                           font_size=36,
    #                           x=window.width // 2, y=window.height // 2,
    #                           anchor_x='center', anchor_y='center')
    # label.draw()


pyglet.clock.schedule_interval(update_frames, 1/60)

pyglet.app.run()