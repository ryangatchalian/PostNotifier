import praw
import settings
import datetime as dt
import pandas as pd
import mysql.connector


def get_date(date: float):
    return dt.datetime.fromtimestamp(date)


def reddit_scrape():
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
    post_data['created'] = post_data['created'].astype(str)

    # Create a list of tuples to be returned.
    output_list = []
    for row in post_data.itertuples():
        output_list.append((row[1], row[2], row[3]))

    return output_list


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.width', None)
# print(post_data)

# for row in post_data.itertuples():
#     print(row[1], row[2], row[3])
