from flask import Flask, render_template, request
import twitter
import re
from secret import *

app = Flask(__name__)
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

def get_user_posts(username):
    global api
    posts = api.GetUserTimeline(screen_name=username)
    posts = [p.text for p in posts]
    return posts

def extract_url(string):
    return re.search(r'(https?://[^\s]+)', string)

def get_fakeness_index(url):
    return 1

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
            return render_template('posts.html', rows=rows)

        except twitter.error.TwitterError:
            return render_template('error.html', message='Username not found.')
