"""

This module contains filter functions to modify images

"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
from textwrap import wrap

import numpy as np
import colorsys
import random

def flip(img):
    """ flip an image head over heels """
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def blur(source_img):
    """ apply gaussian blur to the image """
    return img.filter(ImageFilter.BLUR)


def sort(img, fn=None, amount=None, horizontal=True, reverse=False):
    """ pixel sorting using numpy """

    # get image dimensions
    ymax, xmax = img.size

    # if no amount of sorting is given, sort to the max
    if amount is None:
        if horizontal:
            amount = xmax
        else:
            amount = ymax

    if fn is None:
        fn = brightness

    # lets work with arrays and numpy ...
    a1 = np.asarray(img)
    a2 = np.zeros((xmax, ymax, 3))

    # sorting columns of pixels
    if horizontal is True:

        # create a list of sorting points for partial sorting
        # sample = random.sample(range(ymax), amount)

        # iterate over all the rows
        for x in range(xmax):
            row = a1[x,:,:]
            a2[x,:,:] = sorted(row, key=fn, reverse=reverse)
            # a2[x,:,:] = np.sort(row, axis=0)
            # a2[x,:,:] = np.partition(row, sample, axis=0)


    # sorting rows of pixels
    else:

        # create a list of sorting points for partial sorting
        # sample = random.sample(range(xmax), amount)

        # iterate over all columns
        for y in range(ymax):
            col = a1[:,y,:]
            a2[:,y,:] = sorted(col, key=fn, reverse=reverse)
            # a2[:,y,:] = np.sort(col, axis=0)
            # a2[:,y,:] = np.partition(col, sample, axis=0)


    # turn the array back into an image
    a2 = np.uint8(a2)
    out = Image.fromarray(a2)

    # return the result
    return out

# a couple of functions that determine the order of colors
def brightness(c):
    """ assign a value to each color """
    r, g, b = c
    return 0.299 * r + 0.587 * g + 0.114 * b

def redness(c):
    """ return the amount of red """
    r, g, b = c
    return r

def yellowness(c):
    """ return the amount of yellow """
   
    return r * 0.5 + g * 0.5

def hue(c):
    """ return the hue of some color """
    r, g, b = c
    h, s, v = colorsys.rgb_to_hsv(float(r), float(g), float(b))
    return h


if __name__ == "__main__":

    # load a test image
    img = Image.open("test.jpg")

    # filter the image
    # img = blur(img)
    img = sort(img, fn=hue, reverse=True, horizontal=True)


    # show it
    img.show()




