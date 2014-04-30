#!/usr/bin/env python
from gi.repository import Clutter, GLib
import cairo


def rounded_rect(ctx, x, y, w, h, r):
    ctx.move_to(x + r, y)
    ctx.line_to(x + w - r, y)
    ctx.curve_to(x + w, y, x + w, y, x + w, y + r)
    ctx.line_to(x + w, y + h - r)
    ctx.curve_to(x + w, y + h, x + w, y + h, x + w - r, y + h)
    ctx.line_to(x + r, y + h)
    ctx.curve_to(x, y + h, x, y + h, x, y + h - r)
    ctx.line_to(x, y + r)
    ctx.curve_to(x, y, x, y, x + r, y)

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class CairoActor(Clutter.Actor):
    '''a horizontal item inside a row'''

    def __init__(self):
        super(CairoActor, self).__init__()
        self.set_background_color(color('white'))
        self.set_margin_top(50)
        self.set_margin_right(50)
        self.set_margin_bottom(50)
        self.set_margin_left(50)
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.canvas.connect('draw', self.draw)

        self.idle_resize_id = 0
        self.connect('notify::allocation', self.on_allocation)
        self.canvas.invalidate()

    def on_allocation(self, *_):
        if self.idle_resize_id == 0:
            self.idle_resize_id = Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, 100, self.idle_resize)

    def idle_resize(self):
        self.canvas.invalidate()
        self.canvas.set_size(*self.get_size())
        self.idle_resize_id = 0

    def draw(self, canvas, ctx, width, height):
        ctx.set_operator(cairo.OPERATOR_OVER)
        rounded_rect(
            ctx,
            0,
            0,
            width,
            height,
            100
        )
        ctx.set_source_rgb(0.86, 0.08, 0.24)  # crimson
        ctx.fill_preserve()
        ctx.set_line_width(5)
        ctx.set_source_rgb(0.8, 0.27, 0)  # orange red
        ctx.stroke()

        return True


def stage_key(element, event):
    if event.keyval == Clutter.Escape:
        clutter_quit()


def clutter_quit(*args):
    Clutter.main_quit()

if __name__ == '__main__':
    Clutter.init([])
    stage = Clutter.Stage()
    stage.set_size(800, 500)
    stage.set_title('Clutter - Cairo content')
    stage.set_background_color(color('white'))
    stage.set_user_resizable(True)

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
