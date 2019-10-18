from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import tweepy
from tensorflow import keras
import tensorflow_hub as hub
import os

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
app = Flask(__name__)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


@app.route('/')
def index():
    '''Render the landing page for the website'''
    return render_template('index.html', tweets=[])

@app.route('/topic', methods=['POST'])
def search_tweets():
    '''Get tweets from twitter search api and process sentiment'''
    query = request.form.get('query')
    tweets = [tweet.text for tweet in api.search(q=query, lang='en', rpp=10)]
    return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)