
import cStringIO
import urllib2
from PIL import Image

def get_image_files(tweet):
	""" return the images attached to a tweet """

	images = []
	urls = get_image_urls(tweet)

	for url in urls:

		# get the filename
		filename = url.split('/')[-1]

		# download it and load it into memory
		fd = urllib2.urlopen(url)
		file = cStringIO.StringIO(fd.read())

		# append filename and file to our list of images
		images.append((filename, file))

	return images

def get_image_file(tweet):
	files = get_image_files(tweet)
	if len(files) > 0:
		return get_image_files(tweet)[0]
	else:
		return None

def get_image_urls(tweet):
	# TODO implement this!
	# return "http://www.google.de/images/srpr/logo11w.png"

	urls = []

	for media in tweet.entities.get("media",[{}]):
	    if media.get("type", None) == "photo":
			urls.append(media["media_url"])
	
	return urls


if __name__ == "__main__":

	import tweepy

	# authenticate
	from keys import *
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# get a tweet that contains an image:
	# https://twitter.com/twitter/status/607989490137722882
	api = tweepy.API(auth)
	tweet = api.get_status("607989490137722882")
	media, file = get_image_file(tweet)

	# open the file with PIL and show it
	img = Image.open(file)
	img.show()

