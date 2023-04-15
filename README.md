# Daily-Proverbs-bot

This is a Twitter bot that tweets proverbs from the book ["Colloquial Proverbs"](https://www.hindawi.org/books/75241938/) by Ahmed Taymur Pasha. The bot reads the proverbs and their explanations from a Google Sheet and tweets them out in a threaded manner, with each chunk of the explanation being a reply to the previous tweet.

## Technologies Used

The bot uses the following technologies:

- [gspread](https://gspread.readthedocs.io/en/latest/) - Google Sheets API
- [tweepy](https://www.tweepy.org/) - Twitter API
- [dotenv](https://pypi.org/project/python-dotenv/) - Load environment variables from .env file
- [oauth2client](https://github.com/googleapis/oauth2client) - Google API Authentication
- [datetime](https://docs.python.org/3/library/datetime.html) - Get the current date and time
- [time](https://docs.python.org/3/library/time.html) - Pause between tweets

## How it Works

The bot reads the proverbs and their explanations from a Google Sheet and checks if a tweet has already been posted by looking for the flag (🟩) in the third column. If the tweet has already been posted, the bot skips to the next row.

If the tweet has not been posted, the bot splits the explanation into chunks of 240 characters or less and tweets the proverb. The bot then replies to the proverb with the first chunk of the explanation. The remaining chunks of the explanation are tweeted as replies to the previous tweet.

After the tweet has been posted, the bot updates the Google Sheet with the current date and time and changes the flag to indicate that the tweet has been posted. The bot then waits for 2 minutes before posting the next tweet.
