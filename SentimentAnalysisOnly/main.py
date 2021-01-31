import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt

class App:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def getdata(self):
        ckey = ''
        csecret = ''
        atoken = ''
        atsecret = ''
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, atsecret)
        api = tweepy.API(auth)

        keyword = input("Keyword: ")
        nbtweets = int(input("How many tweets: "))

        self.tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(nbtweets)

        polarity = 0
        pos = 0
        qpos = 0
        vpos = 0
        neg = 0
        qneg = 0
        vneg = 0
        neutral = 0

        for tweet in self.tweets:
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                qpos += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                pos += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                vpos += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                qneg += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                neg += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                vneg += 1

        pos = self.perc(pos, nbtweets)
        qpos = self.perc(qpos, nbtweets)
        vpos = self.perc(vpos, nbtweets)
        neg = self.perc(neg, nbtweets)
        qneg = self.perc(qneg, nbtweets)
        vneg = self.perc(vneg, nbtweets)
        neutral = self.perc(neutral, nbtweets)

        polarity = polarity / nbtweets

        print("Overall sentiment: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Quite positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Very positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Quite negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Very negative")

        self.chart(pos, qpos, vpos, neg, qneg, vneg, neutral, keyword, nbtweets)

    def perc(self, p, w):
        temp = 100 * float(p) / float(w)
        return format(temp, '.2f')

    def chart(self, pos, qpos, vpos, neg, qneg, vneg, neutral, keyword, nbtweets):
        labels = ['Positive', 'Quite positive','Very positive', 'Neutral', 'Negative', 'Quite negative', 'Very negative']
        sizes = [pos, qpos, vpos, neutral, neg, qneg, vneg]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'grey', 'red', 'lightsalmon', 'darkred']
        explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
        centre_circle = plt.Circle((0, 0), 1, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Sentiments of ' + str(nbtweets) + ' tweets about ' + '"' + keyword + '"')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__" :
    app = App()
    app.getdata()
