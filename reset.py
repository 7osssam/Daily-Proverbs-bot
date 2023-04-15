# Description: Deletes all tweets from a Twitter account
# The easiest way to do it while testing  :P (I don't recommend using this)

import tweepy
import os
from dotenv import load_dotenv  # Load environment variables from .env file

load_dotenv()  # Load the environment variables from .env file

# Get twitter API keys from environment variables in .env file
consumer_key = os.environ["API_KEY"]
consumer_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Get all tweets from user's timeline
all_tweets = tweepy.Cursor(api.user_timeline).items()

# Iterate through each tweet and delete it
for tweet in all_tweets:
    api.destroy_status(tweet.id)
