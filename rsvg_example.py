#!/usr/bin/env python
from gi.repository import Clutter, Rsvg
import cairo

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class CairoActor(Clutter.Actor):
    '''a horizontal item inside a row'''

    def __init__(self):
        super(CairoActor, self).__init__()
        self.set_background_color(color('orange'))
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.canvas.connect('draw', self.draw)

        svg = Rsvg.Handle.new_from_file('awesome_tiger.svg')
        self.tiger = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
        svg.render_cairo(cairo.Context(self.tiger))

        self.connect('notify::allocation', self.on_allocation)

    def on_allocation(self, *_):
        self.canvas.set_size(*self.get_size())

    def draw(self, canvas, ctx, width, height):
        ctx.scale(0.5, 0.5)
        ctx.translate(50, 50)
        ctx.set_source_surface(self.tiger, 0, 0)
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.paint()


def stage_key(element, event):
    if event.keyval == Clutter.Escape:
        clutter_quit()


def clutter_quit(*args):
    Clutter.main_quit()

if __name__ == '__main__':
    Clutter.init([])
    stage = Clutter.Stage()
    stage.set_size(500, 500)
    stage.set_title('Clutter - SVG Content')
    stage.set_background_color(color('white'))

    # quit when the window gets closed
    stage.connect('destroy', clutter_quit)

    # close window on escape
    stage.connect('key-press-event', stage_key)

    cairo_actor = CairoActor()
    stage.add_child(cairo_actor)

    # bind the size of cairo_actor to the size of the stage
    cairo_actor.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

    stage.show()
    Clutter.main()
