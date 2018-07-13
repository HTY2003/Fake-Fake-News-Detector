import re
from flask import Flask, render_template, request
from random import randint
import twitter
from secret import *

app = Flask(__name__)
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret,
                  tweet_mode='extended')

def get_user_posts(username):
    global api
    posts = api.GetUserTimeline(screen_name=username, count=200)
    posts = [p.full_text for p in posts]
    return posts

def extract_url(string):
    return re.search(r'(https?://[^\s]+)', string)

def get_fakeness_index(url):
    return randint(-10, 11)

@app.route('/')
def mainpage():
    return render_template('mainpage.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        result = request.form
        username = result['username']
        try:
            posts = get_user_posts(username)
            posts_with_urls = []
            for p in posts:
                url = extract_url(p)
                if url:
                    posts_with_urls.append((p, url))

            rows = [(get_fakeness_index(url), p) for p, url in posts_with_urls]
            print(rows[1])
            return render_template('posts.html', rows=rows, username=username)

        except twitter.error.TwitterError:
            return render_template('error.html', message='Username not found.')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    pass
