from gi.repository import Clutter, Cogl
from ninepatch import ninepatch

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


class NinePatchActor(Clutter.Actor):
    '''9 patch actor'''
    __gtype_name__ = 'NinePatchActor'

    def __init__(self, image_filename):
        super(NinePatchActor, self).__init__()
        self.ninepatch = ninepatch.Ninepatch(image_filename)

        self.connect('notify::allocation', self.on_allocation)

    def on_allocation(self, *_):
        image = Clutter.Image()
        try:
            scaled_image = self.ninepatch.render(int(self.get_width()), int(self.get_height()))

            image.set_data(
                scaled_image.tostring(),
                Cogl.PixelFormat.RGBA_8888,
                self.get_width(),
                self.get_height(),
                self.get_width() * 4,
            )

            self.set_content_scaling_filters(
                Clutter.ScalingFilter.TRILINEAR,
                Clutter.ScalingFilter.LINEAR
            )
            self.set_content(image)

        except ninepatch.ScaleError:
            pass  # just scale the last computed image down


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

    nine_patch_actor = NinePatchActor('ninepatch/9patch_test.png')
    margin = 50
    nine_patch_actor.set_margin_top(margin)
    nine_patch_actor.set_margin_right(margin)
    nine_patch_actor.set_margin_bottom(margin)
    nine_patch_actor.set_margin_left(margin)

    container.add_child(nine_patch_actor)
    stage.add_child(container)

    # bind the size of cairo_actor to the size of the stage
    container.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))
    nine_patch_actor.add_constraint(Clutter.BindConstraint.new(container, Clutter.BindCoordinate.SIZE, 0.0))

    stage.show()
    Clutter.main()
