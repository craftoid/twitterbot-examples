import tweepy
import keys
import webbrowser

# create auth handler
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)

# go to redirect URL to get a pin code
try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
except tweepy.TweepError:
    print("Error! Failed to get request token.")

# Let the owner of the twitter account enter the pin code
webbrowser.open(redirect_url)
pincode = raw_input("Enter PIN Code >>> ")

# grant access to the app
try:
	auth.get_access_token(pincode)
except tweepy.TweepError:
	print("Error! Failed to get access token.")

# print access tokens
print('access_token = "{}"'.format(auth.access_token))
print('access_token_secret = "{}"'.format(auth.access_token_secret))
