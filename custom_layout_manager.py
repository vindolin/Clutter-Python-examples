#!/usr/bin/env python
from gi.repository import Clutter, GLib
from random import randint, random

VISIBLE_ROWS = 8
TOTAL_ROWS = 50
MINIMUM_CONTENT_HEIGHT = 200

color = lambda string: Clutter.color_from_string(string)[1]  # shortcut


def random_color(random_alpha=False):
    rgb = [randint(0, 255) for x in range(3)]
    rgba = rgb + [randint(0, 255) if random_alpha else 255]
    return Clutter.Color.new(*rgba)


class VBox(Clutter.Actor):
    '''the root element inside stage'''

    def __init__(self):
        super(VBox, self).__init__()
        self.layout = Clutter.BoxLayout.new()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(self.layout)
        self.set_background_color(color('grey'))

        self.header = Header()
        self.content = Content()
        self.footer = Footer()

        self.add_child(self.header)
        self.add_child(self.content)
        self.add_child(self.footer)


class Header(Clutter.Actor):
    '''fixed height header'''

    def __init__(self):
        super(Header, self).__init__()
        self.set_background_color(color('red'))
        self.set_height(80)
        self.set_x_expand(True)


class ContentLayoutManager(Clutter.LayoutManager):
    '''this layout manager manages the rows inside content'''

    def __init__(self):
        super(ContentLayoutManager, self).__init__()

    def do_get_preferred_height(self, actor, for_width):
        return MINIMUM_CONTENT_HEIGHT, 0  # min_height, preferred_height

    def do_get_preferred_width(self, actor, for_height):
        return 0, 0

    def do_allocate(self, actor, box, flags):
        for i, row in enumerate(actor.get_children()):
            row_box = Clutter.ActorBox()
            row_height = box.get_height() / VISIBLE_ROWS

            row_box.x1 = box.x1
            row_box.x2 = box.x2
            row_box.y1 = row_height * i
            row_box.y2 = (row_height * i) + row_height

            row.allocate(row_box, flags)


class RowLayoutManager(Clutter.LayoutManager):
    '''this layout manager manages the items inside a row'''

    def __init__(self):
        super(RowLayoutManager, self).__init__()

    def do_get_preferred_height(self, actor, for_width):
        return 0, 0

    def do_get_preferred_width(self, actor, for_height):
        return 0, 0

    def do_allocate(self, actor, box, flags):
        x1 = 0
        for item in actor.get_children():
            item_box = Clutter.ActorBox()

            item_width = item.length * box.get_width()

            item_box.x1 = x1
            item_box.x2 = x1 + item_width
            item_box.y1 = 0
            item_box.y2 = box.get_height()

            item.allocate(item_box, flags)

            x1 += item_width


class Content(Clutter.ScrollActor):
    '''the center element inside VBox that holds the rows'''

    def __init__(self):
        super(Content, self).__init__()

        self.layout = ContentLayoutManager()
        self.set_layout_manager(self.layout)
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.set_background_color(color('gray'))
        self.row_layout = RowLayoutManager()  # gets reused by all rows
        self.update()

    def update(self):
        self.destroy_all_children()  # oh noes, all teh children!

        for i in range(TOTAL_ROWS):
            row = Row()
            row.set_layout_manager(self.row_layout)

            total_length = 0
            while True:  # add items until total length is 1
                item = Item(random() / 3)
                total_length += item.length
                row.add_child(item)
                if total_length >= 1.0:
                    item.length -= total_length - 1.0
                    break

            self.add_child(row)

        return True


class Row(Clutter.Actor):
    '''a row that holds items'''

    def __init__(self):
        super(Row, self).__init__()
        self.set_background_color(random_color())
        self.set_x_expand(True)


class Footer(Clutter.Actor):
    '''fixed height footer'''

    def __init__(self):
        super(Footer, self).__init__()
        self.set_background_color(color('blue'))
        self.set_height(100)
        self.set_x_expand(True)


class Item(Clutter.Actor):
    '''a horizontal item inside a row'''

    def __init__(self, length):
        super(Item, self).__init__()
        self.set_background_color(random_color())
        self.length = length


def stage_key(element, event):
    if event.keyval == Clutter.Escape:
        clutter_quit()


def clutter_quit(*args):
    Clutter.main_quit()


if __name__ == '__main__':
    Clutter.init([])
    stage = Clutter.Stage()
    stage.set_size(800, 500)
    stage.set_title('Clutter - custom layout managers')
    stage.set_user_resizable(True)

    # quit when the window gets closed
    stage.connect('destroy', clutter_quit)

    # close window on escape
    stage.connect('key-press-event', stage_key)

    vbox = VBox()
    stage.add_child(vbox)

    # bind the size of vbox to the size of the stage
    vbox.add_constraint(Clutter.BindConstraint.new(stage, Clutter.BindCoordinate.SIZE, 0.0))

    # update the content of vbox every 4 seconds
    Clutter.threads_add_timeout(GLib.PRIORITY_DEFAULT, 4000, vbox.content.update)

    stage.show()
    Clutter.main()
