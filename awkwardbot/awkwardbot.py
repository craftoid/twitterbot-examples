#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

# make sure to use unicode for python3 compatibility
from __future__ import unicode_literals

# argument parsing
from sys import argv


# twitterbot framework
from twitterbot import TwitterBot

# improved logging + random functions
import logging, random

# load keys for the twitter API
import keys

# image functions
import image

# google query functions
import google


class AwkwardBot(TwitterBot):
	"""
	This bot tweets an image from awkwardfamiliyphotos.com every minute
	"""

	# Run the bot in debug mode, so we get some interactive feedback
	debug = True

	# file with image urls

	def __init__(self):

		# default initalization
		TwitterBot.__init__(self)

		# load image urls from a file
		self.load_image_urls("images.txt")


	def load_image_urls(self, image_file):	
		"""
		load a list of image urls from a local file
		"""
	
		with open(image_file) as f:
			self.image_urls = [line.strip() for line in f.readlines()]
		self.log("Found {} Images".format(len(self.image_urls)))

		# if the list of image urls has changed the image id may be out of range.
		# let's make sure this does not happen...
		if(self.state['last_image_id'] >= len(self.image_urls)):
			self.log("last_image_id out of range. Resetting it to 0", logging.ERROR)
			self.state["last_image_id"] = 0


	def bot_init(self):
		"""
		Initialize and configure the bot
		"""

		############################
		# REQUIRED: LOGIN DETAILS! #
		############################
		self.config['api_key'] = keys.consumer_key	
		self.config['api_secret'] = keys.consumer_secret
		self.config['access_key'] = keys.access_token
		self.config['access_secret'] = keys.access_token_secret


		######################################
		# SEMI-OPTIONAL: OTHER CONFIG STUFF! #
		######################################

		# how often to tweet, in seconds (30 seconds minimum)
		self.config['tweet_interval'] = 1 * 60     # default: run once a minute

		# use this to define a (min, max) random range of how often to tweet
		# e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
		self.config['tweet_interval_range'] = None

		# only reply to tweets that specifically mention the bot
		self.config['reply_direct_mention_only'] = True

		# only include bot followers (and original tweeter) in @-replies
		self.config['reply_followers_only'] = False

		# fav any tweets that mention this bot?
		self.config['autofav_mentions'] = False

		# fav any tweets containing these keywords?
		self.config['autofav_keywords'] = []

		# follow back all followers?
		self.config['autofollow'] = False

		# State variable - will only be set if we are not loading a previously saved state 
		self.state['last_image_id'] = 0

		self.log("Custom Initalization Complete")
		

	def log(self, message, loglevel=logging.INFO):
		"""
		improved logging for debug mode
		"""

		if loglevel == logging.ERROR:
			logging.error(message)
			if self.debug:
				print("ERROR: " + message)
		elif loglevel == logging.INFO:
			logging.info(message)
			if self.debug:
				print("INFO: " + message)
			

	def _show_state(self):
		"""
		Debugging method to show the current bot state
		"""
		for key, value in self.state.items():
			print("{}: {}".format(key, value))

	def on_scheduled_tweet(self):
		"""
		Make a public tweet to the bot's own timeline.
		"""
		
		print("Posting next tweet")

		# get image id
		image_id = self.state['last_image_id']

		# get image url
		url = self.image_urls[image_id]
		print("Image URL: {}".format(url))

		# load image
		file = image.load_image(url)

		# get filename
		filename = url.split('/')[-1]

		# get some awkward text
		text = self.create_awkward_text()

		# post image tweet
		self.post_tweet(text, media=filename, file=file)

		# update bot state, picking the next image id
		self.state['last_image_id'] = (image_id + 1) % len(self.image_urls)

	def create_awkward_text(self):
		"""
		Use google autocomplete to create awkward questions ...
		"""	
	
		# pick a random awkward word
		awkward_list = [ "creepy", "awkward", "disgusting" ]
		word = random.choice(awkward_list)
	
		# create the first couple of words for a google query	
		incomplete = "How {} is".format(word)

		# create a question using google autocomplete
		queries = google.autocomplete(incomplete)
		query = random.choice(queries).capitalize() + "?"

		# return tweet text
		return "{question}\nAsk google: {url} #awkwardquestion".format(
			question=query,
			url=google.query_url(query)
		)


	def on_mention(self, tweet, prefix):
		"""
		Actions to take when a mention is received.
		"""
		pass # don't do anything here ...


	def on_timeline(self, tweet, prefix):
		"""
		Actions to take on a timeline tweet.
		"""
		pass # Don't do anything here ...

	def destroy_all_tweets(self):
		""" 
		Delete everything we ever tweeted
		"""
		total = 0
		while True:
			# Maximum number of tweets we can get at once is 800
			# See https://dev.twitter.com/rest/reference/get/statuses/home_timeline
			timeline = self.api.user_timeline(count=800)
			n = len(timeline)
			if n > 0:
				print("Deleting {} tweets.".format(n))
				for tweet in timeline:
					self.api.destroy_status(tweet.id)
				total += n
			else:
				print("Done.")
				break

		self.log("Deleted {} tweets".format(total))

if __name__ == '__main__':
	

	# no arguments given?
	if len(argv) == 1:

		# print usage info
		print( "USAGE: {} run | tweet | clean | info ".format(argv[0]) )

	else:
		# get the command
		cmd = argv[1]

		# create the bot
		bot = AwkwardBot()
		

		if cmd == "run":
			# run the bot
			bot.log("Running the bot")
			bot.run()
			
		if cmd == "tweet":
			# just post a single tweet
			bot.log("Posting a tweet")
			bot.on_scheduled_tweet()

			# save state before we exit
			bot._save_state()

		if cmd == "clean":
			# remove all tweets
			bot.log("Removing all tweets")
			bot.destroy_all_tweets()
			
			# save state before we exit
			bot._save_state()

		if cmd == "info":
			print("Current bot state")
			bot._show_state()
