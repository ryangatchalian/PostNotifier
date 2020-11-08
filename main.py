# General Note: Web scraping is good, because you don't have to rely on any API.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# Path to chromedriver, which is used to drive the chrome browser when web scraping.
DRIVER_PATH = r"C:\Users\iRuni\IdeaProjects\PostNotifier\chromedriver"
LINK = 'https://newjersey.craigslist.org/d/free-stuff/search/zip'
BASE_LINK = 'https://newjersey.craigslist.org'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")

# takes an instance of the chromedriver through 'options', and uses driver path to navigate
# to the chromedriver location
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get(LINK)
# using BS, we obtain the page's html as a string.
soup = BeautifulSoup(driver.page_source, 'html.parser')


def next_page(url: str):
    """ Gets the next page's html """
    driver.get(BASE_LINK + url)
    return BeautifulSoup(driver.page_source, 'html.parser')


def get_posts(new_soup: BeautifulSoup, post_list: list):
    """ Gets all the posts on current page, and adds to given list """
    all_posts = new_soup.findAll('li', class_='result-row')
    for post in all_posts:
        post_list.append(post)


# gets the total number of posts
totalPosts = soup.find('span', class_='totalcount').text
# gets the next url
nextButton = soup.find('a', class_='button next')
# list for all the titles of each posting
all_titles = []
# Add the current page's post titles to the list
get_posts(soup, all_titles)

# go through each page, and add the post titles to the list
while True:
    if nextButton.get('href'):
        latest_soup = next_page(nextButton.get('href'))
        nextButton = latest_soup.find('a', class_='button next')
        get_posts(latest_soup, all_titles)
    else:
        break

for i, posting in enumerate(all_titles):
    postTitle = post.find('a', class_='result-title').get_text()
    postTime = post.find('time').get('title')
    print("{}: {}: {}".format(i + 1, postTime, postTitle))

print(len(all_titles))

driver.quit()

# with open('all_posts.txt', 'w') as all_posts:
#     for page_posts in all_titles:
#         try:
#             print(page_posts, file=all_posts)
#         except UnicodeEncodeError:
#             print("theres something here I swear", file=all_posts)
