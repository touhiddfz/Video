from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Function to get video sources from a URL
def get_video_sources(url):
    # Set up Selenium to use Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Path to your ChromeDriver
    chrome_service = Service("/path/to/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Load the webpage
    driver.get(url)
    
    # Wait for the page to load completely and for JavaScript to render the content
    time.sleep(5)  # Adjust this as needed

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all video tags and extract their source URLs
    video_sources = []
    for video_tag in soup.find_all('video'):
        source_tag = video_tag.find('source')
        if source_tag:
            video_sources.append(source_tag.get('src'))

    # Close the browser
    driver.quit()

    return video_sources

# Example usage
url = input("Enter the webpage URL: ")
videos = get_video_sources(url)
if videos:
    print("Video sources found:")
    for video in videos:
        print(video)
else:
    print("No video sources found.")
    