#!/usr/bin/env python

from gi.repository import Clutter, Cogl
import ninepatch

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class NinePatchActor(Clutter.Actor):
    '''9 patch actor'''
    __gtype_name__ = 'NinePatchActor'

    def __init__(self, image_filename, stage=None):
        super(NinePatchActor, self).__init__()
        self.ninepatch = ninepatch.Ninepatch(image_filename)
        self.stage = stage
        if self.stage:
            self.old_stage_title = self.stage.get_title()

        self.connect('notify::allocation', self.on_allocation)

    def on_allocation(self, *_):
        image = Clutter.Image()
        try:
            scaled_image = self.ninepatch.render(int(self.get_width()), int(self.get_height()))

            image.set_data(
                data=scaled_image.tostring(),
                pixel_format=Cogl.PixelFormat.RGBA_8888,
                width=self.get_width(),
                height=self.get_height(),
                row_stride=self.get_width() * 4,
            )

            self.set_content(image)
            if self.stage:
                self.stage.set_title(self.old_stage_title)

        except ninepatch.ScaleError:
            if self.stage:
                self.stage.set_title('9 Patch is undersized!')


if __name__ == '__main__':

    color = lambda string: Clutter.color_from_string(string)[1]  # shortcut

    def stage_key(element, event):
        if event.keyval == Clutter.Escape:
            clutter_quit()

    def clutter_quit(*args):
        Clutter.main_quit()

    Clutter.init([])
    stage = Clutter.Stage()
    stage.set_size(800, 500)
    stage.set_title('Clutter - 9 Patch Actor')
    stage.set_user_resizable(True)

    # quit when the window gets closed
    stage.connect('destroy', clutter_quit)

    # close window on escape
    stage.connect('key-press-event', stage_key)

    container = Clutter.Actor()
    container.set_background_color(color('pink'))

    nine_patch_actor = NinePatchActor('9patch_bubble.png', stage)
    margin = 50
    nine_patch_actor.set_margin_top(margin)
    nine_patch_actor.set_margin_right(margin)
    nine_patch_actor.set_margin_bottom(margin)
    nine_patch_actor.set_margin_left(margin)

    container.add_child(nine_patch_actor)
    stage.add_child(container)

    # bind the size of cairo_actor to the size of the stage
    container.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0))
    nine_patch_actor.add_constraint(Clutter.BindConstraint.new(container, Clutter.BindCoordinate.SIZE, 0))

    stage.show()
    Clutter.main()
