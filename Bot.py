import gspread  # Google Sheets API
import tweepy  # Twitter API

import time
from oauth2client.service_account import ServiceAccountCredentials  # Google Sheets API
from datetime import datetime  # Get the current date and time

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

# Authenticate with Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'Google_credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet and select the first worksheet
sheet = client.open('TwitterBot2').worksheet('XYZ')

# Open the "Posted" worksheet
posted_sheet = client.open('TwitterBot2').worksheet('Posted')

# Get all the values from the worksheet
values = sheet.get_all_values()


values = values[1:]  # exclude header row

for row in values:
    phrase = row[0]
    explanation = row[1]
    isPosted = row[2]  # Get the flag from column C

    # Check if the tweet has already been posted by checking the flag
    if isPosted == '🟩':
        continue  # Skip this row and move to the next one

    # Split the explanation into chunks of 250 characters or less
    words = explanation.split()
    chunks = []
    chunk = ""
    for word in words:
        if len(chunk) + len(word) + 1 <= 240:
            chunk += word + " "
        else:
            chunks.append(chunk.strip())
            chunk = word + " "
    if chunk:
        chunks.append(chunk.strip())

    # Tweet the phrase and reply with the first chunk of the explanation
    tweet = api.update_status(phrase)
    reply_tweet = api.update_status(status="(1/" + str(len(chunks)) + ") " + chunks[0], in_reply_to_status_id=tweet.id,
                                    auto_populate_reply_metadata=True)

    # Loop through the remaining chunks of the explanation and reply to the previous tweet
    for i, chunk in enumerate(chunks[1:], start=2):
        reply_tweet = api.update_status(status="(" + str(i) + "/" + str(len(chunks)) + ") " + chunk, in_reply_to_status_id=reply_tweet.id,
                                        auto_populate_reply_metadata=True)

    # Get the current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write the posted tweet to the "Posted" worksheet with the current date and time
    posted_sheet.append_row([phrase, explanation, now])

    # Set the value of the third column to '🟩' for the posted tweet
    # add 2 to exclude header row and 0-based indexing
    row_index = values.index(row) + 2
    sheet.update_cell(row_index, 3, '🟩')

    # Wait for 2 minutes before posting the next tweet
    # time.sleep(120)

    # wait for 2 hours before posting the next tweet
    # time.sleep(7200)
