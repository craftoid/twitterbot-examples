from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import math


def c64screen(text, petscii=False, invert=False, shift=False, pixel_size=2):
    """ simulate a C64 screen """

    # c64 color scheme
    fg_color = (160, 160, 255)
    bg_color = (64, 64, 225)

    # screen estate
    screen_size = 320, 200

    # vertical and horizontal border size
    border_size = 32, 32 + 60

    # total monitor size
    monitor_size = tuple(m + 2 * b for m, b in zip(screen_size, border_size))

	# create an image containing the complete monitor
    bg_image = Image.new('RGBA', monitor_size, fg_color)

	# get drawing context for the screen
    ctx = ImageDraw.Draw(bg_image)

    # calculate screen coordinates
    top_left = border_size
    bottom_right = tuple(m + b - 1 for m, b in zip(screen_size, border_size))

    # draw screen rectangle
    ctx.rectangle((top_left, bottom_right), fill=bg_color)

    # let's use an 8 bit C64 pixel font
    font = ImageFont.truetype('pixel.ttf', 8)

    # generate greeting
    greeting = [
        "                                        ",
        "    **** COMMODORE 64 BASIC V2 ****     ",
        "                                        ",
        " 64 K RAM SYSTEM 38911 BASIC BYTES FREE ",
        "                                        "
    ]

    # split text into lines that are no longer than 40 chars
    c64lines = []
    for line in text.splitlines():
        for i in xrange(0, len(line), 40):
            c64lines.append(line[i:i+40])

    # cursor position
    x, y = top_left

    # unicode offset
    unipage, SHIFT, INVERT = 0xe000, 0x100, 0x200

    # select unicode page for shifted chars
    if shift:
        unipage |= SHIFT

    # print greeting
    for line in greeting:
        # transpose characters to PETSCII
        if petscii:
            line = "".join([unichr(unipage|ord(c)) for c in line])
        # render text
        ctx.text((x, y), line, font=font, fill=fg_color)
        # move cursor to the next line
        y += 8

    # select unicode page for inverted chars
    if invert:
        unipage |= INVERT

    # draw the text
    for line in c64lines:
        # transpose characters to PETSCII
        if petscii:
            line = "".join([unichr(unipage|ord(c)) for c in line])
        # render text
        ctx.text((x, y), line, font=font, fill=fg_color)
        # move cursor to the next line
        y += 8

    # calculate scaled size
    scaled_size = tuple(int(m * pixel_size) for m in monitor_size)

    # use antialiasing for non integer pixel sizes
    if pixel_size % 1 > 0:
        scaling = Image.ANTIALIAS
    else:
        scaling = Image.NEAREST

    # resize the image
    bg_image = bg_image.resize(scaled_size, scaling)

    # return the final image
    return bg_image


if __name__ == "__main__":

    # show a single screen
    c64screen(' I s COMMODORE 64 ...', petscii=True).show()

    # show inverted characters
    img = c64screen("\n".join((
        "                  ",
        " I s COMMODORE 64 ",
        "                  "
    )), petscii=True, invert=True).show()

    # show typing simulation
    # c64animation('I s COMMODORE 64 ...', petscii=True, ivnert=True).show()

