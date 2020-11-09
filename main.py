# General Note: Web scraping is good, because you don't have to rely on any API.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import *


def next_page(wbdriver: webdriver, url: str):
    """ Gets the next page's html """
    wbdriver.get(BASE_LINK + url)
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
    for i, posting in enumerate(all_posts):
        post = posting.find('a', class_='result-title')
        post_title = post.get_text()
        post_link = post.get('href')
        post_timedata = posting.find('time').get('datetime')
        post_time = datetime.strptime(post_timedata, '%Y-%m-%d %H:%M')
        time_since = (datetime.now() - post_time)
        days_since, hours_since, mins_since = elapsed_time(time_since)
        print("{}:\t {}\n\t\t\t\t\t\t {} \n\t\t\t\t\t\t {} Days {} Hours {} Minutes Ago".format(
            post_time, post_title, post_link, days_since, hours_since, mins_since))


# Path to chromedriver, which is used to drive the chrome browser when web scraping.
DRIVER_PATH = r"D:\Documents\PostNotifier-main\PostNotifier-main\chromedriver"
LINK = 'https://newjersey.craigslist.org/d/free-stuff/search/zip'
BASE_LINK = 'https://newjersey.craigslist.org'
KEYWORD = 'circleline'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

# takes an instance of the chromedriver through 'options', and uses driver path to navigate
# to the chromedriver location
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(LINK)
# using BS, we obtain the page's html as a string.
soup = BeautifulSoup(driver.page_source, 'html.parser')

# gets the total number of posts
totalPosts = soup.find('span', class_='totalcount').text
# gets the next url
nextButton = soup.find('a', class_='button next')
# list for all the titles of each posting
all_titles = []
# Add the current page's post titles to the list
get_posts(soup, all_titles, search=KEYWORD)

# go through each page, and add the post titles to the list
while True:
    if nextButton.get('href'):
        latest_soup = next_page(driver, nextButton.get('href'))
        nextButton = latest_soup.find('a', class_='button next')
        get_posts(latest_soup, all_titles, search=KEYWORD)
    else:
        break

output_results(all_titles)
# for i, posting in enumerate(all_titles):
#     postTitle = posting.find('a', class_='result-title').get_text()
#     postTimeData = posting.find('time').get('datetime')
#     postTime = datetime.strptime(postTimeData, '%Y-%m-%d %H:%M')
#     timeSince = (datetime.now() - postTime)
#     daysSince, hoursSince, minSince = elapsed_time(timeSince)
#     print("{}:\t {}\n\t\t\t\t\t\t {} Days {} Hours {} Minutes Ago".format(
#         postTime, postTitle, daysSince, hoursSince, minSince))


print("{} results containing {}".format(len(all_titles), KEYWORD))

driver.quit()
