from splinter import Browser
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False) 
    return browser

def scrape_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].get_text()
    news_title
    news_p= soup.find_all('div', class_='article_teaser_body')[0].get_text()
    news_p



    df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts = df.to_html()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    link = browser.links.find_by_partial_text("FULL IMAGE")[0].click()
    link
    link = browser.links.find_by_partial_text("more info")[0].click()
    link
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find_all('figure', class_="lede")[0]
    featured_image_url = "https://www.jpl.nasa.gov"+ image.select_one("a img").get("src")
    featured_image_url

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    links = browser.links.find_by_partial_text("Hemisphere")
    hemisphere_images_urls = []
    for l in range(len(links)):
        browser.links.find_by_partial_text("Hemisphere")[l].click()
        hemisphere = {}
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url = browser.links.find_by_text("Sample").first["href"]
        image_text = soup.find_all('h2', class_="title")[0].get_text()
    #image_url = image.select_one("a href").get("src")
        hemisphere["img_url"] = image_url
        hemisphere["title"] = image_text
        hemisphere_images_urls.append(hemisphere)
        print(hemisphere_images_urls)
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_urls":hemisphere_images_urls

    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
