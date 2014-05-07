from PIL import Image
import numpy as np


class ScaleError(Exception):
    pass


def find_marks(image):
    '''find the cut marks'''
    data = np.asarray(image)

    x_marks = [0, 0]
    y_marks = [0, 0]

    black = np.array([0, 0, 0, 255])

    for marks in [x_marks, y_marks]:

        data = data.swapaxes(0, 1)

        # search first occurence
        for i, items in enumerate(data):
            if np.array_equal(items[0], black):
                marks[0] = i
                break

        # reverse search last occurence
        for i, items in enumerate(data[::-1]):
            if np.array_equal(items[0], black):
                marks[1] = len(data) - i
                break

    #TODO sanity checks
    return {'x': x_marks, 'y': y_marks}


def slice_image(im):
    '''slice a 9 patch image'''
    marks = find_marks(im)

    # add normalized cut marks
    x_marks = (1, marks['x'][0], marks['x'][1] + 1, im.size[0] + 1)
    y_marks = (1, marks['y'][0], marks['y'][1] + 1, im.size[1] + 1)

    pieces = [[0 for x in range(3)] for y in range(3)]
    for x in range(len(x_marks) - 1):
        for y in range(len(y_marks) - 1):
            pieces[x][y] = im.crop((x_marks[x], y_marks[y], x_marks[x + 1] - 1, y_marks[y + 1] - 1))

    return pieces


def scale_image(filename, width, height, filter=Image.ANTIALIAS):
    im = Image.open(filename)
    '''slices an image an scales the scalable pieces'''

    pieces = slice_image(im)

    min_width = pieces[0][0].size[0] + pieces[2][0].size[0]
    min_height = pieces[0][0].size[1] + pieces[0][2].size[1]
    center_width = width - min_width
    center_height = height - min_height

    if width <= min_width + 1 or height <= min_height + 1:
        # FIXME scale down to min_size
        raise ScaleError('cannot scale down')

    scaled_im = Image.new('RGBA', (width, height), None)

    # TODO, this is hackish :(

    # corners
    scaled_im.paste(pieces[0][0], (0, 0))
    scaled_im.paste(pieces[2][0], (width - pieces[2][0].size[0], 0))
    scaled_im.paste(pieces[0][2], (0, height - pieces[0][2].size[1]))
    scaled_im.paste(pieces[2][2], (width - pieces[2][0].size[0], height - pieces[0][2].size[1]))

    # center
    scaled_im.paste(pieces[1][1].resize((center_width, center_height), filter), (pieces[0][0].size[0], pieces[0][0].size[1]))

    # scaled pieces
    scaled_im.paste(pieces[1][0].resize((center_width, pieces[1][0].size[1]), filter), (pieces[0][0].size[0], 0))
    scaled_im.paste(pieces[1][2].resize((center_width, pieces[1][2].size[1]), filter), (pieces[0][0].size[0], height - pieces[0][2].size[1]))

    scaled_im.paste(pieces[0][1].resize((pieces[0][1].size[0], center_height), filter), (0, pieces[0][0].size[1]))
    scaled_im.paste(pieces[2][1].resize((pieces[2][1].size[0], center_height), filter), (pieces[0][0].size[0] + center_width, pieces[0][0].size[1]))

    return scaled_im


if __name__ == '__main__':

    scale_image('../epg/assets/9patch_test.png', 200, 500).show()
