#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot
from illustrator import c64screen
import keys

class PicBot(TwitterBot):
    """
    Whenever you tweet a sentence at this bot, it will tweet back at you with an image
    containing the sentence, with some words replaced by images
    """
    def bot_init(self):
        """ Initialize and configure the bot """

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
        self.config['tweet_interval'] = 1 * 60     # default: 1 minutes

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


    def on_scheduled_tweet(self):
        """ Make a public tweet to the bot's own timeline. """
        # We might take senteces from somewhere and tweet them on a regular basis ...
        pass # don't do anything here ...


    def on_mention(self, tweet, prefix):
        """ Actions to take when a mention is received. """
        
        tweetsize = 140 - len(prefix) - 1

        try:
            # default tweet text
            response = "{}, your image is ready.".format(prefix)

            # create a tweet and make sure to cut it off at 140 chars
            text = prefix + " " + response
            text = text[:140]

            # post the tweet
            self.post_(text, reply_to=tweet)

        except Exception as e:
        	# did anything go wrong when we tried to create and post the tweet?
            print(e)


    def on_timeline(self, tweet, prefix):
        """ Actions to take on a timeline tweet. """
        pass # Don't do anything here ...



if __name__ == '__main__':
    bot = PicBot()
    bot.run()
