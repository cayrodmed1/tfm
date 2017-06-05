import json
import tweepy
import string

from pykafka import KafkaClient

# Twitter API tokens
ACCESS_TOKEN = 'XXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXX'
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXX'

# Listener class to be used by tweepy
class StdOutListener(tweepy.StreamListener):

    # When a tweet comes, send attributes 'created_at' and 'screen_name' to Kafka
    def on_status(self, status):
        date = str(status.created_at)
        user = status._json['user']['screen_name']
        msg = date + "|" + user
        with mytopic.get_sync_producer() as producer:
            producer.produce(str(msg))
        return True


    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

# Main function
if __name__ == '__main__':

    listener = StdOutListener()

    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Create twitter stream using OAuth credentials and the listener
    stream = tweepy.Stream(oauth, listener)

    # We need to specify the Kafka server
    client = KafkaClient(hosts="tfmkafka.ddns.net:9092")
    
    # This is the topic in the Kafka broker
    mytopic = client.topics['twitter']

    # Here we can filter tweets by any word
    stream.filter(track=['#RussianGP'])
