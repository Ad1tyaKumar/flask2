"""
Created on Sun Apr  2 10:43:54 2023
#chage
@author: HP
"""


from flask import Flask, jsonify
from gnews import GNews
from newspaper import Article
from textblob import TextBlob
import nltk
import requests
nltk.download('punkt')
from flask_cors import CORS, cross_origin

#text = "Ram Navami"


app = Flask(__name__)
CORS(app)
google_news = GNews()


# API_URL = "https://api-inference.huggingface.co/models/Amite5h/TextClassificationmulticlass"
# headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

# output = query({
# 	"inputs": "I like you. I love you",
# })

classifiy = ["Business" , "Entertainment" , "Politics" , "Sports" , "Tech"]
def label(output):
  a = output[0][0]["label"]
  a = int(a[6])
  return classifiy[a]



@app.route('/')
@cross_origin(supports_credentials=True)
def home():
    return "Hello World"

@app.route('/search/<text>',methods=['GET','POST'])
def search(text):
    '''
    For direct API calls trought request
    '''
    news = google_news.get_news(text)
    json = []
    count = 0
    for i in range(len(news)):
      try:
        url = news[i]['url']
        head = news[i]['title']

        # download and parse article
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.text
        summary = article.summary
        blob = TextBlob(summary)
#         output = query({"inputs": summary })
#         Textlabel = label(output)
        senti = "Positive" if blob.polarity > 0 else "negative" if blob.polarity < 0 else "neutral"
        count+=1
        d = {}
        d["Headline"] = head
        d["Url"] = url
        d["Article"] = text
        d["summary"] = summary
        d["Sentiment"] = senti
        d["images"] = article.top_image
        d["Publish date"] = article.publish_date
        d["Keywords"] = article.keywords
        d["TextClassification"] = "Sports"
        d["id"] = count
        json.append(d)
      except:
        continue
    return jsonify(json)


@app.route('/topic_wise/<n>',methods=['GET','POST'])
def topic_wise(n):
    '''
    For direct API calls trought request
    '''
    topic = ["WORLD", "NATION","BUSINESS","TECHNOLOGY","ENTERTAINMENT","SPORTS","SCIENCE","HEALTH"]
    topic_news = google_news.get_news_by_topic(topic[int(n)])
    json = []
    count = 0
    for i in range(len(topic_news)):

      try:
        url = topic_news[i]['url']
        head = topic_news[i]['title']

        # download and parse article
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.text
        summary = article.summary
        blob = TextBlob(summary)
        output = query({"inputs": summary })
        Textlabel = label(output)
        senti = "Positive" if blob.polarity > 0 else "negative" if blob.polarity < 0 else "neutral"
        count+=1
        d = {}
        d["Headline"] = head
        d["Url"] = url
        d["Article"] = text
        d["sentiment"] = senti
        d["images"] = article.top_image
        d["Summary"] = summary
        d["Publish date"] = article.publish_date
        d["Keywords"] = article.keywords
        d["TextClassification"] = Textlabel
        d["id"] = count
        json.append(d)
      except:
        continue
    return jsonify(json)


#route for top news
@app.route('/top_news',methods=['GET','POST'])
def top_news():
    '''
    For direct API calls trought request
    '''
    news = google_news.get_top_news()
    json = []
    count = 0
    for i in range(len(news)):
      try:
        url = news[i]['url']
        head = news[i]['title']

        # download and parse article
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.text
        summary = article.summary
        blob = TextBlob(summary)
        output = query({"inputs": summary })
        Textlabel = label(output)
        senti = "Positive" if blob.polarity > 0 else "negative" if blob.polarity < 0 else "neutral"
        count+=1
        d = {}
        d["Headline"] = head
        d["Url"] = url
        d["Article"] = text
        d["summary"] = summary
        d["Sentiment"] = senti
        d["images"] = article.top_image
        d["Publish date"] = article.publish_date
        d["Keywords"] = article.keywords
        d["TextClassification"] = Textlabel
        d["id"] = count
        json.append(d)
      except:
        continue
    return jsonify(json)


#route for top news
@app.route('/local',methods=['GET','POST'])
def local():
    '''
    For direct API calls trought request
    '''
    news = google_news.get_news_by_location("Ranchi")
    json = []
    count = 0
    for i in range(len(news)):
      try:
        url = news[i]['url']
        head = news[i]['title']

        # download and parse article
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        text = article.text
        summary = article.summary
        blob = TextBlob(summary)
        output = query({"inputs": summary })
        Textlabel = label(output)
        senti = "Positive" if blob.polarity > 0 else "negative" if blob.polarity < 0 else "neutral"
        count+=1
        d = {}
        d["Headline"] = head
        d["Url"] = url
        d["Article"] = text
        d["summary"] = summary
        d["Sentiment"] = senti
        d["images"] = article.top_image
        d["Publish date"] = article.publish_date
        d["Keywords"] = article.keywords
        d["TextClassification"] = Textlabel
        d["id"] = count
        json.append(d)
      except:
        continue
    return jsonify(json)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
