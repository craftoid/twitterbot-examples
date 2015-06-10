#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from twitterbot import TwitterBot
from c64 import c64screen
import random
import keys
from cStringIO import StringIO


class C64Bot(TwitterBot):
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
        self.config['reply_followers_only'] = True

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = False

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = []

        # follow back all followers?
        self.config['autofollow'] = False


    def on_scheduled_tweet(self):
        """ Make a public tweet to the bot's own timeline. """
        # We might take senteces from somewhere and tweet them on a regular basis ...

        quote = "10 GOTO {}".format(10 * random.randint(2, 100))
        print("Posting to timeline: {}".format(quote))
        self.post_image(quote)


    def on_mention(self, tweet, prefix):
        """ Actions to take when a mention is received. """
  
        # ignore for now
        return


        tweetsize = 140 - len(prefix) - 1

        try:
            # default tweet text
            response = "{}, your image is ready.".format(prefix)

            # create a tweet and make sure to cut it off at 140 chars
            response = response[:140]

            # post the tweet
            # self.post_tweet(response, reply_to=tweet)
            self.post_image(response, reply_to=tweet)

        except Exception as e:
        	
        	# did anything go wrong when we tried to create and post the tweet?
            print(e)


    def on_timeline(self, tweet, prefix):
        """ Actions to take on a timeline tweet. """
        pass # Don't do anything here ...


    def post_image(self, text, reply_to=None):
        """ create a picture from the tweet and post it """ 

        # create a C64 screen shot from the text
        image = c64screen(text)

        # turn the image into a string
        output = StringIO()
        image.save(output, format="PNG")

        # post text + image
        print("posting image ({})".format(text))
        self.post_tweet(text, media="output.png", file=output, reply_to=reply_to)

        output.close()

 

if __name__ == '__main__':
    bot = C64Bot()
    bot.run()
