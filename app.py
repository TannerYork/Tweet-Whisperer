# Imports for running web-server and recieving tweets
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import tweepy
import os

# Imports for tweet processing
from tensorflow import keras
import tensorflow_hub as hub
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import preprocessor as p
import re

# Load Twitter API keys
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Setup tweepy api
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Initialize app valiables
app = Flask(__name__)
stop_words = set(stopwords.words('english'))
model = keras.models.load_model('./tweet_sa_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

@app.route('/')
def index():
    '''Render the landing page for the website'''
    return render_template('index.html')

@app.route('/topic', methods=['POST'])
def search_tweets():
    '''Get tweets from twitter search api and process sentiment'''
    query = request.form.get('query')
    tweets = [tweet.text for tweet in api.search(q=query, lang='en', count=100)]
    sentiment_data = get_sentiment_data(tweets)
    return render_template('index.html', sentiment_data=sentiment_data)

def preprocess_tweets(tweets):
    ''' Preprocesses tweets by removing special characters, removing urls, lowercasing, and 
        removing stop words form the tweets text
            Args:
                tweets: a list of dictionaries with tweet information
            Returns:
                A list of preprocessed tweets\' text
    '''
    proccessed_tweets = []
    for text in tweets:
        text = p.clean(text)
        text = re.sub(r'@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', text.lower()).strip()
        new_text = [token for token in word_tokenize(text) if token not in stop_words and len(token) > 1]
        proccessed_tweets.append(' '.join(new_text))
    return proccessed_tweets

def get_sentiment_data(tweets):
    '''
    A function for getting the overall attitude from a set of tweets
        Args:
            tweets: a list of dictionaries with tweet information
        Returns:
            A list of preprocessed tweets\' text
    '''
    tweets = preprocess_tweets(tweets)
    total_pos = 0
    total_neg = 0
    processed_data = {}
    for text in tweets:
        perdiction = model.predict([text])
        if perdiction[0][0] < .5: 
            total_neg += 1
        elif perdiction[0][0] > .5: 
            total_pos += 1
    processed_data['total_attitude'] = 'Positive' if total_pos > total_neg else 'Negative'
    return processed_data

if __name__ == '__main__':
    app.run(debug=True)