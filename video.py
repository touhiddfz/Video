import requests
from bs4 import BeautifulSoup
import os

# Function to extract H1 title and google drive URLs from a page
def extract_info_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract H1 title
        h1_title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No H1 Title'
        
        # Extract Google Drive URLs
        google_drive_urls = []
        for link in soup.find_all('a', href=True):
            if 'drive.google.com' in link['href']:
                google_drive_urls.append(link['href'])
                
        return h1_title, google_drive_urls
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None, []

# Function to crawl sitemap and extract required information
def crawl_sitemap(sitemap_url, output_file):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')

        urls = soup.find_all('loc')
        
        with open(output_file, 'w') as f:
            for url in urls:
                page_url = url.get_text()
                h1_title, google_drive_urls = extract_info_from_url(page_url)
                
                if google_drive_urls:
                    f.write(f"H1 Title: {h1_title}\n")
                    for drive_url in google_drive_urls:
                        f.write(f"Google Drive URL: {drive_url}\n")
                    f.write("\n")
        
        print("Save Complete")
    except Exception as e:
        print(f"Save Failed: {e}")

# Input sitemap URL
sitemap_url = input("Enter the XML Sitemap URL: ")

# Set the output file path
output_file = '/storage/emulated/0/Download/anime.txt'

# Crawl the sitemap and save the results
crawl_sitemap(sitemap_url, output_file)
    
