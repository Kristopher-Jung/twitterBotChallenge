import tweepy
from datetime import datetime
from inputHandler import *

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
    '@' + handle  # respond to @mentions
]

# override the default listener to add code to on_status
class MyStreamListener(tweepy.StreamListener):

    # listener for tweets
    # -------------------
    # this function will be called any time a tweet comes in
    # that contains words from the array created above
    def on_status(self, status):
        #log the incoming tweet
        print('[{}] Received: "{}" from @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.text,
            status.author.screen_name
        ))

        # get the text from the tweet mentioning the bot.
        # for this bot, we won't need this since it doesn't process the tweet.
        # but if your bot does, then you'll want to use this
        userInput = status.text
        userId = status.author.screen_name

        # after processing the input, you can build your output
        # into this variable. again, since we're just reply "No.",
        # we'll just set it as that.

        handler = inputHandler(userInput, userId)
        response = handler.recordAndResponse()


        talkTo = '@'+userId+' '
        # respond to the tweet
        api.update_status(
            status=talkTo+response,
            in_reply_to_status_id=status.id
        )

        print('[{}] Responded to @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.author.screen_name
        ))


# create a stream to receive tweets
try:
    streamListener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener)
    stream.filter(track=trigger_words)
except KeyboardInterrupt:
    print('\nGoodbye')
