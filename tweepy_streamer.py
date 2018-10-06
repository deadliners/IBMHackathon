#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "795915228965801984-VuY9ZT7M35gyRxqAVAnTKYxb5Vf0CVu"
access_token_secret = "UagpdXAAGWEb1AV80iPKoBv5eWjNR75xroFlQ8Ty5ApHJ"
consumer_key = "b1JpbUxE9KDYQVkFKmnGPrGK4"
consumer_secret = "JJsinTA93wOet2SivmYcdXdwO6LojUJ4qbqeewPNr68osptNU3"

####TWIITER STREAMER#####
class TwitterStreamer() :

    """
    Class for streaming and processing live tweets
    """

    def stream_tweets(self , fetched_tweets_filename , hash_tag_list) :
       #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)

        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=hash_tag_list)                  
        

####TWITTER STREAMER LISTENER####
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    """
    This is a basic listener class that just prints recieved tweets to stdout
    """

    def __init__(self, fetched_tweets_filename ) :
        self.fetched_tweets_filename = fetched_tweets_filename 

    def on_data(self, data):
        try :
            print(data)
            with open(self.fetched_tweets_filename , 'a') as tf :
                tf.write(data)
            return True
        except BaseException as E :
            print ("Error on data : %s" % str(E))
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    hash_tag_list = ["Donald Trump" , "India" , "Spicy" ]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename , hash_tag_list)
