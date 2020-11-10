# General Note: Web scraping is good, because you don't have to rely on any API.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import *
import pandas as pd
import settings


def next_page(wbdriver: webdriver, url: str):
    """ Gets the next page's html """
    wbdriver.get(settings.BASE_LINK + url)
    return BeautifulSoup(wbdriver.page_source, 'html.parser')


def get_posts(new_soup: BeautifulSoup, post_list: list, search=''):
    """ Gets all the posts on current page, and adds to given list """
    all_posts = new_soup.findAll('li', class_='result-row')
    for post in all_posts:
        post_title = post.find('a', class_='result-title').get_text()
        if search.casefold() in post_title.casefold():
            post_list.append(post)


def elapsed_time(time_passed: timedelta):
    """ Converts timedelta to days, hours, and minutes """
    days = time_passed.days
    hours = time_passed.seconds//3600
    minutes = (time_passed.seconds//60) % 60
    return days, hours, minutes


def output_results(all_posts: list):
    post_dict = {'title': [],
                 'url': [],
                 'created': []}
    for posting in all_posts:
        post = posting.find('a', class_='result-title')
        post_timedata = posting.find('time').get('datetime')
        post_time = datetime.strptime(post_timedata, '%Y-%m-%d %H:%M')
        post_dict['title'].append(post.get_text())
        post_dict['url'].append(post.get('href'))
        post_dict['created'].append(post_time)
    post_data = pd.DataFrame(post_dict)
    print(post_data)


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

# takes an instance of the chromedriver through 'options', and uses driver path to navigate
# to the chromedriver location
driver = webdriver.Chrome(options=options, executable_path=settings.DRIVER_PATH)
driver.get(settings.LINK)
# using BS, we obtain the page's html as a string.
soup = BeautifulSoup(driver.page_source, 'html.parser')

totalPosts = soup.find('span', class_='totalcount').text
nextButton = soup.find('a', class_='button next')
all_titles = []

# Add the current page's post titles to the list
get_posts(soup, all_titles, search=settings.CRAIGSLIST_KEYWORD)

# go through each page, and add the post titles to the list
while True:
    if nextButton.get('href'):
        latest_soup = next_page(driver, nextButton.get('href'))
        nextButton = latest_soup.find('a', class_='button next')
        get_posts(latest_soup, all_titles, search=settings.CRAIGSLIST_KEYWORD)
    else:
        break

output_results(all_titles)

print("{} results containing {}".format(len(all_titles), settings.CRAIGSLIST_KEYWORD))

driver.quit()
