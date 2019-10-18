from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/')
def index():
    '''Render the landing page for the website'''
    return render_template('index.html', topic=None)

@app.route('/topic', methods=['POST'])
def search_tweets():
    '''Get tweets from twitter search api and process sentiment'''
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)