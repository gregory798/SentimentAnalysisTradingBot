import tweepy
import time
from textblob import TextBlob
import yfinance as yf
import xlsxwriter

ckey = ""
csecret = ""
atoken = ""
atsecret = ""
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, atsecret)
api2 = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def perc(a,b):
    temp = 100 * float(a) / float(b)
    return format(temp, '.2f')


def get_twitter_BTC():
    ratios = 0
    nb = 500

    keyword1 = "BTC"
    keyword2 = "#BTC"
    keyword3 = "Bitcoin"
    keywords = [keyword1, keyword2, keyword3]

    for keyword in keywords:
        tweets = tweepy.Cursor(api2.search, q=keyword, lang="en").items(nb)

        pos = 0
        neg = 0

        for tweet in tweets:
            analysis = TextBlob(tweet.text)

            if 0 <= analysis.sentiment.polarity <= 1:
                pos += 1
            elif -1 <= analysis.sentiment.polarity < 0:
                neg += 1

        pos = perc(pos, nb)
        neg = perc(neg, nb)

        if float(neg) > 0:
            ratio = float(pos) / float(neg)
        else:
            ratio = float(pos)
        ratios += ratio
    return ratios


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


if __name__ == "__main__":
    print("Bot working...")
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'BUY BTC at :')
    worksheet.write(0, 1, 'SELL BTC at :')
    worksheet.write(0, 2, 'PROFIT (%)')
    worksheet.set_column(0, 0, 25)
    worksheet.set_column(1, 1, 25)
    worksheet.set_column(2, 2, 10)
    row = 1
    ct = 0

    while True:
        if ct == 10:
            workbook.close()
            print("Bot finished")
            break
        score = get_twitter_BTC()
        min1 = score + (score * 30 / 100)
        time.sleep(60*10)
        new_score = get_twitter_BTC()

        if new_score > min1:
            btc_price = get_current_price("BTC-USD")
            worksheet.write(row, 0, btc_price)
            time.sleep(60*10)
            new_new_score = get_twitter_BTC()
            min2 = new_new_score - (new_new_score * 30 / 100)
            if new_new_score < new_score:
                new_btc_price = get_current_price("BTC-USD")
                trade_profit = new_btc_price - btc_price
                perc_profit = trade_profit / btc_price * 100
                perc_profit_round = round(perc_profit, 3)
                worksheet.write(row, 1, new_btc_price)
                worksheet.write(row, 2, perc_profit_round)
                time.sleep(60*5)
            row += 1
            ct += 1
        else:
            time.sleep(60*10)
