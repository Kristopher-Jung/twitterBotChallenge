import tweepy
from datetime import datetime
import os

if os.path.isfile('./secret.py'):
    from secret import consumer_key, consumer_secret, access_token, access_secret, handle
else:
    if os.environ.get("handle"):
        handle = os.environ.get("handle")
    if os.environ.get("TWBOT_ACCESS_SECRET"):
        access_secret = os.environ.get("TWBOT_ACCESS_SECRET")
    if os.environ.get("TWBOT_ACCESS_TOKEN"):
        access_token = os.environ.get("TWBOT_ACCESS_TOKEN")
    if os.environ.get("TWBOT_CON_KEY"):
        consumer_key = os.environ.get("TWBOT_CON_KEY")
    if os.environ.get("TWBOT_CON_SECRET"):
        consumer_secret = os.environ.get("TWBOT_CON_SECRET")

# get authentication info
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# log into the API
api = tweepy.API(auth)
print('[{}] Logged into Twitter API as @{}\n-----------'.format(
    datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
    handle
))

# string array of words that will trigger the on_status function
trigger_words = [
    '@' + handle # respond to @mentions
]

# override the default listener to add code to on_status
class MyStreamListener(tweepy.StreamListener):

    # listener for tweets
    # -------------------
    # this function will be called any time a tweet comes in
    # that contains words from the array created above
    def on_status(self, status):

        # log the incoming tweet
        print('[{}] Received: "{}" from @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.text,
            status.author.screen_name
        ))

        # get the text from the tweet mentioning the bot.
        # for this bot, we won't need this since it doesn't process the tweet.
        # but if your bot does, then you'll want to use this
        message = status.text

        # after processing the input, you can build your output
        # into this variable. again, since we're just reply "No.",
        # we'll just set it as that.
        response = "No."

        # respond to the tweet
        api.update_status(
            status=response,
            in_reply_to_status_id=status.id
        )

        print('[{}] Responded to @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.author.screen_name
        ))

# create a stream to receive tweets
try:
    streamListener = MyStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(track=trigger_words)
except KeyboardInterrupt:
    print('\nGoodbye')