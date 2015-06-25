#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

import keys
from twitterbot import TwitterBot

class ExtrovertBot(TwitterBot):
	def bot_init(self):
		"""
		Initialize and configure your bot!

		Use this function to set options and initialize your own custom bot
		state (if any).
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

		# how often to tweet, in seconds
		self.config['tweet_interval'] = 1 * 60     # default: 1 minute

		# use this to define a (min, max) random range of how often to tweet
		# e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
		self.config['tweet_interval_range'] = None

		# only reply to tweets that specifically mention the bot
		self.config['reply_direct_mention_only'] = False

		# only include bot followers (and original tweeter) in @-replies
		self.config['reply_followers_only'] = True

		# fav any tweets that mention this bot?
		self.config['autofav_mentions'] = False

		# fav any tweets containing these keywords?
		self.config['autofav_keywords'] = []

		# follow back all followers?
		self.config['autofollow'] = False

		# list of tweets we already replied to
		self.state['replied_tweets'] = []


		print("SETUP: Replied tweets: {}".format(self.state['replied_tweets']))

	def on_scheduled_tweet(self):
		"""
		Make a public tweet to the bot's own timeline.

		It's up to you to ensure that it's less than 140 characters.

		Set tweet frequency in seconds with TWEET_INTERVAL in config.py.
		"""

		# do a twitter search for tweets containing the word "summer"
		tweet = self.search_tweet_containing("summer2020")

		print("Checking for new people to annoy ...")

		if tweet:

			print("Found tweet, check if we already replied to it ...")
			print(tweet.text)

			# only return the tweet if we haven't replied to it yet

			if tweet in self.state['replied_tweets']:
				print("Encountered the tweet before...")
				return

			else:

				# YAY, lets reply!!!
				print("Found a tweet I did not reply to, yet")
				# compose a reply to the tweet
				prefix = tweet.author.screen_name
				text = "@{} Don't forget the sunscreen!".format(prefix)

				# add tweet to list of replied tweets
				self.state['replied_tweets'].append(tweet)

				# post it
				self.post_tweet(text, reply_to=tweet)


	def on_mention(self, tweet, prefix):
		"""
		...
		"""
		return

	def on_timeline(self, tweet, prefix):
		"""
		...
		"""
		return

	def search_tweet_containing(self, word):
		"""
		Returns one tweet from the list of tweets that contain the word
		"""
		api = self.api

		# get a single tweet, not a whole list
		result = api.search(word, rpp=1)

		# just some debugging output
		for tweet in result:
			print(tweet.text)

		# get tweet from the list, containing only one tweet
		if result:

			tweet = result[0]
			return tweet

		else:
			return None


if __name__ == '__main__':
	bot = ExtrovertBot()

	bot.run()

	# tweet = bot.search_tweet_containing("summeriliciousfunkyboots")
	
	# if tweet:
	# 	print(tweet.text)
	# else:
	# 	print("No tweet found...")

