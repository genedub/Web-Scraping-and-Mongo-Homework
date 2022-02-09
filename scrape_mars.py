import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
# browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    list_hemisphere = {}

    url = 'https://redplanetscience.com/#'

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    url2 = 'https://spaceimages-mars.com/'

    browser.visit(url2)
    
    image = browser.find_by_css('.fancybox-thumbs').links.find_by_partial_href('image/mars/').first

    featured_image_url = image['href']

    data = pd.read_html("https://galaxyfacts-mars.com/")[0]

    data.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
    
    data.set_index("Mars-Earth Comparison",inplace=True)

    mongo_data = data.to_html()

    url3 = 'https://marshemispheres.com/'

    browser.visit(url3)

    links_found = browser.find_by_css('.product-item img')

    url_images = []
    
    for i in range(len(links_found)):
        url_images.append(links_found[i]['src'])


    scrape_results = {"images": url_images,
                      "title": news_title,
                      "news": news_p,
                      "data": data
                      "mongo_data": mongo_data
                        }

    browser.quit()

    return scrape_results



