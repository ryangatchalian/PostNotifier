import praw
import settings
import datetime as dt
import pandas as pd


def get_date(date: float):
    return dt.datetime.fromtimestamp(date)


# connection to reddit
reddit = praw.Reddit(client_id=settings.ID_NUMBER,
                     client_secret=settings.SECRET_NUMBER,
                     user_agent=settings.APP_NAME,
                     username=settings.USER,
                     password=settings.PASS)

# specify targetted subreddit
subreddit = reddit.subreddit(settings.SUBREDDIT)

# search subreddit for post by keyword, in the past hour
new_subreddit = subreddit.search(settings.REDDIT_KEYWORD, time_filter='day')

post_dict = {'title': [],
             'url': [],
             'created': []}

for post in new_subreddit:
    post_dict['title'].append(post.title)
    post_dict['url'].append(post.url)
    post_dict['created'].append(get_date(post.created))

post_data = pd.DataFrame(post_dict)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
print(post_data)
