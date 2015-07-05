import StringIO
import urllib2

def load_image(url):
	""" load image file from the WWW into memory """
	fd = urllib2.urlopen(url)
	return StringIO.StringIO(fd.read())
