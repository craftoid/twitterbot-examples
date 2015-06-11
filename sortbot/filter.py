"""

This module contains filter functions to modify images

"""

from PIL import Image, ImageDraw, ImageFilter, ImageColor
from textwrap import wrap

import numpy as np
import colorsys
import random

r = 100

def flip(img):
    """ flip an image head over heels """
    return img.transpose(Image.FLIP_TOP_BOTTOM)


def blur(source_img):
    """ apply gaussian blur to the image """
    return img.filter(ImageFilter.BLUR)

def process_lines(img, fn=None, amount=10, horizontal=True):
    """ shift rows or columns of pixels """

    if fn is None:
        fn = shift_list

    # get image dimensions
    ymax, xmax = img.size

    # lets work with arrays and numpy ...
    a1 = np.asarray(img)
    a2 = np.zeros((xmax, ymax, 3))

    # shifting columns of pixels
    if horizontal is True:

        # iterate over half of the rows
        for x in range(xmax / 2):
            d = random.randint(-amount, amount)
            row = a1[x,:,:]
            a2[x,:,:] = fn(row, d)

        # iterate over the other half
        for x in range(xmax / 2, xmax):
            a2[x,:,:] = a1[x,:,:]

    # sorting rows of pixels
    else:

        # iterate over all columns
        for y in range(ymax / 2):
            d = random.randint(-amount, amount)
            col = a1[:,y,:]
            a2[:,y,:] = fn(col, d)

        # iterate over the other half
        for y in range(ymax / 2, ymax):
            a2[:,y,:] = a1[:,y,:]

  
    # turn the array back into an image
    a2 = np.uint8(a2)
    out = Image.fromarray(a2)

    # return the result
    return out

def shift_list(lst, amount):
    """ 
    shift list by amount to the left
    shift_list([1,2,3,4,5], 2)
    [3,4,5,1,2]
    """
    # make sure we got lists
    lst = list(lst)

    # combine slices
    lst = lst[amount:] + lst[:amount]
    return lst

def sort(img, fn=None, horizontal=True, reverse=False):
    """ pixel sorting using numpy """

    # get image dimensions
    ymax, xmax = img.size

    if fn is None:
        fn = brightness

    # lets work with arrays and numpy ...
    a1 = np.asarray(img)
    a2 = np.zeros((xmax, ymax, 3))

    # sorting columns of pixels
    if horizontal is True:

        # iterate over all the rows
        for x in range(0, xmax):
            row = a1[x,:,:]
            a2[x,:,:] = sorted(row, key=fn, reverse=reverse)

    # sorting rows of pixels
    else:

        # iterate over all columns
        for y in range(ymax):
            col = a1[:,y,:]
            a2[:,y,:] = sorted(col, key=fn, reverse=reverse)
  
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
    r, g, b = c
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
    img = process_lines(img, amount=5, horizontal=False)

    # once more
    img = process_lines(img, amount=5, horizontal=True)

    # show it
    img.show()


