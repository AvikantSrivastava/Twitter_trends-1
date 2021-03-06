import os
from textblob import TextBlob
import tweepy



class SentimentEngine():
    def __init__(self, TrendName):

        # Authentication
        auth = tweepy.OAuthHandler(
            os.environ['API_KEY'],
            os.environ['API_SECRET_KEY'])

        auth.set_access_token(
            os.environ['ACCESS_TOKEN'],
            os.environ['ACCESS_TOKEN_SECRET'])

        self.api = tweepy.API(auth ,timeout=15)


        self.Trend = TrendName
        self.Tweets = []

        search_query = self.Trend

        for tweet_object in tweepy.Cursor(self.api.search,q=search_query+" -filter:retweets",lang='en',result_type='recent').items(100):
            self.Tweets.append(tweet_object.text)

        self.positive = self.negative = 0

        for tweet in self.Tweets:
            analysis = TextBlob(tweet)
            if analysis.sentiment.polarity >= 0.2:
                self.positive+=1
            elif analysis.sentiment.polarity <= -0.2:
                self.negative +=1
        if self.positive == 0 and self.negative == 0:
            self.PositiveScore = 0.50
            self.NegativeScore = 0.50     
        else:
            self.PositiveScore = round(self.positive / (self.positive + self.negative),2)
            self.NegativeScore = round(self.negative / (self.positive + self.negative),2)

    def getScores(self):
        return self.PositiveScore, self.NegativeScore


if __name__ == '__main__':
# mainly for testing

    eminem = SentimentEngine('eminem')
    print(f'Score for Eminem Good {eminem.getScores()[0]} Bad {eminem.getScores()[1]}')

    mkbhd = SentimentEngine('mkbhd')
    print(f'Score for RCB Good {mkbhd.getScores()[0]} Bad {mkbhd.getScores()[1]}')
