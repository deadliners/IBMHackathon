#Import the necessary methods from tweepy library
import tweepy
#from tweepy import API_
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import numpy as np
import pandas as pd
from textblob import TextBlob
import re

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

    def get_twitter_client_api(self):
        return self.twitter_client

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

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self,tweet) :
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," " , tweet).split())

    def analyze_sentiment(self,tweet) :
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0 :
            return "positive"
        elif analysis.sentiment.polarity == 0 :
            return "neutal"
        else :
            return "negative"
    
    def tweets_to_data_frame(seld , tweets) :
        df = pd.DataFrame(data= [tweet.text for tweet in tweets] , columns=['Tweets'])

        df['id'] =  np.array([tweet.id for tweet in tweets ])
        
        return df
    
    
if __name__ == '__main__':
    """
    hash_tag_list = ["Donald Trump" , "India" , "Spicy" ]
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient('pycon')
    print(ascii(twitter_client.get_user_timeline_tweets(1)))

    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename , hash_tag_list)
    """

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name = "realDonaldTrump" , count = 100)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #To print the tweets. Number of tweets depend on count
    #print(ascii(tweets))

    #To print first six tweet's Text
    #print(ascii(df.head()))

    #To print list of attributes of class
    #print(dir.tweet[0])

    #To print the Id of 0th tweet
    #print(tweets[0].id)

    #To print retweet countof 0th tweet 
    #print(tweets[0].retweet_count)
    df['sentiment'] =  np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets'] ])
    
    #To print first six tweet's Text
    print(ascii(df.head(20)))


