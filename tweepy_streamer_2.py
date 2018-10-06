#Import the necessary methods from tweepy library
import tweepy
#from tweepy import API_
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "795915228965801984-VuY9ZT7M35gyRxqAVAnTKYxb5Vf0CVu"
access_token_secret = "UagpdXAAGWEb1AV80iPKoBv5eWjNR75xroFlQ8Ty5ApHJ"
consumer_key = "b1JpbUxE9KDYQVkFKmnGPrGK4"
consumer_secret = "JJsinTA93wOet2SivmYcdXdwO6LojUJ4qbqeewPNr68osptNU3"

####Twitter Client####
class TwitterClient():
    def __init__(self , twitter_user=None) :
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self , num_tweets) :
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline , id = self.twitter_user).items(num_tweets) :
            tweets.append(tweet)
        return tweets

    def get_friend_list(self , num_friends) :
        friend_list = []
        for friend in Cursor(self.twitter_client.friends , id = self.twitter_user).items(num_friends) :
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self,num_tweets) :
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline , id = self.twitter_user).items(num_tweets) :
            homw_timeline_tweets.append(tweet)
        return home_timeline_tweets
    
#### TWITTER AUTHENTICATOR ####
class TwitterAuthenticator() :
    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    

####TWIITER STREAMER#####
class TwitterStreamer() :

    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenicator = TwitterAuthenicator()      

    def stream_tweets(self , fetched_tweets_filename , hash_tag_list) :
       #This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenicator.authenticate_twiiter_app()
        stream = Stream(auth, listener)

        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track=hash_tag_list)                  
        

####TWITTER STREAMER LISTENER####
#This is a basic listener that just prints received tweets to stdout.
class TwitterListener(StreamListener):

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
        if status == 420 :
            #Returning False on_data in case rate limit occurs  
            return False
        print (status)


if __name__ == '__main__':
    hash_tag_list = ["Donald Trump" , "India" , "Spicy" ]
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient('pycon')
    print(ascii(twitter_client.get_user_timeline_tweets(1)))

    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename , hash_tag_list)
