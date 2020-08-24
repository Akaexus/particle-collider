from modules.config import Config
from modules.simulation.engine import Engine
config = Config()

engine = Engine(config)


import pyglet

window = pyglet.window.Window(resizable=True)
pyglet.gl.glClearColor(0.8, 0.8, 0.8, 0.8)
def update_frames(dt):
    global engine
    engine.tick()

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


pyglet.clock.schedule_interval(update_frames, 0.016)

pyglet.app.run()