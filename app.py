import json
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

import tweepy
from random import shuffle

### Twitter API KEY
Consumer_key = 'kGaRMeBr1gj4X5i3XTxvP1jIl'
Consumer_secret = 'Zyg0TJzfCQI89P7cPTSXRuGprjKUyZpbPe6BQ1CDv6g7okc4Bo'
Access_token = '971157695242805248-JJW6I9V3Fsw3fc56npsHfkFR51uxXvH'
Access_secret = 'csB5CQnIQWpzwQJmBIeB5Pm4gLxWOTv15uOPdF6xaxlc3'

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
#     """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""
#     with urlopen("http://feeds.feedburner.com/hatena/b/hotentry") as res:
#         html = res.read().decode("utf-8")
#     soup = BeautifulSoup(html, "html.parser")
#     items = soup.select("item")
#     shuffle(items)
#     item = items[0]
#     print(item)

    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True) # API利用制限にかかった場合、解除まで待機する
    # return(api)

    #つぶやきを格納するリスト
    global tweets_data
    tweets_data =[]
    keyword = '小杉湯 -RT'

    tweets = tweepy.Cursor(api.search, q = keyword ,   # APIの種類と検索文字列
                            include_entities = True,  # 省略されたリンクを全て取得
                            tweet_mode = 'extended',  # 省略されたツイートを全て取得
                            lang = 'ja').items()       # 日本のツイートのみ取得
                            
    for tweet in tweets:
        if tweet.favorite_count + tweet.retweet_count >= 10:
            tweets_data.append(tweet.full_text + '\n')
            shuffle(tweets_data)
            item = tweets_data[0]
            print(item)


    return json.dumps({

                "content" : item,
                "link" :'',
    })

if __name__ == "__main__":
    app.run(debug=True, port=5003)
    # app.run(debug=True, port=5004)