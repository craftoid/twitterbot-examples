#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot
from picbot import PicBot
from PIL import Image, ImageDraw
from sys import argv

import numpy
import cv2

import keys


classifier = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(classifier)


def face_detect(image):
	"""
	Return rectangles of identified face regions
	"""

	# numpy grayscale image for face detection
	array = numpy.asarray(image)
	gray_image = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)

	# tweak this for better results ..

	faces = faceCascade.detectMultiScale(
    	gray_image,
    	scaleFactor=1.1,
    	minNeighbors=5,
    	minSize=(30, 30),
    	flags=cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	# convert boxes from from arrays to tuples
	boxes = [(x, y, x + w, y + h) for (x, y, w, h) in faces]
	return boxes
		

HORIZONTAL = Image.FLIP_TOP_BOTTOM
VERTICAL = Image.FLIP_LEFT_RIGHT

def face_flip(image, direction=HORIZONTAL):
	""" 
	Flip the faces upside-down (or left-to-right) 
	"""

	# work on a copy
	image = image.copy()

	# identify boxes
	boxes = face_detect(image)

	# crop out faces
	faces = [image.crop(rect) for rect in boxes]

	# flip faces
	faces = [face.transpose(direction) for face in faces]

	# paste them back in
	for box, face in zip(boxes, faces):
		image.paste(face, box)

	return image, boxes


def face_swap(image, offset=1):
	"""
	Rotate / swap images
	"""

	# work on a copy
	image = image.copy()

	# identify rectangles
	boxes = face_detect(image)

	# crop out faces
	faces = [image.crop(rect) for rect in boxes]

	# rotate face order
	faces = faces[offset:] + faces[:offset]

	# resize faces to fit the new boxes
	faces = [face.resize((x2-x1, y2-y1), resample=Image.BICUBIC)for (x1, y1, x2, y2), face in zip(boxes, faces)]

	# paste them faces back into the original image
	for box, face in zip(boxes, faces):
		image.paste(face, box)

	return image, boxes


def face_mark(image):
	""" 
	Mark faces with boxes
	"""

	# work on a copy
	image = image.copy()
	
	# identify boxes
	boxes = face_detect(image)

	# get drawing context for the current image
	ctx = ImageDraw.Draw(image)

	# define colors
	black = (0, 0, 0, 255)
	white = (255,255,255,255)

	# draw boxes
	for box in boxes:

		# draw a black box
		ctx.rectangle(box, fill=None, outline=black)

		# draw a white box around it
		x1, y1, x2, y2 = box
		box = x1 - 1, y1 - 1, x2 + 1, y2 + 1
		ctx.rectangle(box, fill=None, outline=white)

	return image, boxes


if __name__ == '__main__':

	print("Loading source image")
	src = Image.open("test2.jpg")
	src.show()

	print("Testing face marking")
	img, boxes = face_mark(src)
	img.show()

	print("Testing face flipping")
	img = Image.open("test2.jpg")
	img, boxes = face_flip(src)
	img.show()

	print("Testing face swapping")
	img, boxes = face_swap(src)
	img.show()


