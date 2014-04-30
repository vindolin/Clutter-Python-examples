#!/usr/bin/env python
from gi.repository import Gtk
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


class CairoTest(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='CairoTest')

        drawing_area = Gtk.DrawingArea()
        drawing_area.connect('draw', self.on_draw)
        self.add(drawing_area)

    def on_draw(self, widget, ctx):
        ctx.set_operator(cairo.OPERATOR_OVER)
        rounded_rect(
            ctx,
            0,
            0,
            widget.get_allocated_width(),
            widget.get_allocated_height(),
            100
        )
        ctx.set_source_rgb(0.86, 0.08, 0.24)  # crimson
        ctx.fill_preserve()
        ctx.set_line_width(5)
        ctx.set_source_rgb(0.8, 0.27, 0)  # orange red
        ctx.stroke()


win = CairoTest()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
