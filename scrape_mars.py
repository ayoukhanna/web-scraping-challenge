from splinter import Browser
from bs4 import BeautifulSoup
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[1].get_text()
    news_title
    df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts = df.to_html()
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
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url":featured_image_url,
        "mars facts":mars_facts,
        "hemisphere urls":hemisphere_images_urls

    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
