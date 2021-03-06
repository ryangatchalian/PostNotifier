import praw
from settings import *
import datetime as dt
import pandas as pd


def get_date(date: float):
    return dt.datetime.fromtimestamp(date)


def reddit_scrape(sub, key):
    # connection to reddit
    reddit = praw.Reddit(client_id=ID_NUMBER,
                         client_secret=SECRET_NUMBER,
                         user_agent=APP_NAME,
                         username=USER,
                         password=PASS)

    # specify targetted subreddit
    subreddit = reddit.subreddit(sub)

    # search subreddit for post by keyword, in the past hour
    new_subreddit = subreddit.search(key, sort='new', time_filter='day')

    post_dict = {'title': [],
                 'url': [],
                 'created': []}

    for post in new_subreddit:
        post_dict['title'].append(post.title)
        post_dict['url'].append(post.url)
        post_dict['created'].append(get_date(post.created))
    post_data = pd.DataFrame(post_dict)
    post_data['created'] = post_data['created'].astype(str)

    # Create a list of tuples to be returned.
    output_list = []
    for row in post_data.itertuples():
        output_list.append((row[1], row[2], row[3]))

    return output_list
