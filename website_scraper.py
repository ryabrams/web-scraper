import requests
from bs4 import BeautifulSoup
import csv
import urllib.parse
import time
import datetime
import logging
from urllib.robotparser import RobotFileParser

# --- Configuration ---
WEBSITE_URL = "YOUR_WEBSITE_URL_HERE"  # <--- Placeholder URL - REPLACE THIS!
DELAY_BETWEEN_REQUESTS = 5  # Seconds
CSV_FILENAME = "scrape_{}.csv" # Filename changed to "scrape_YYYY-MM-DD.csv"
LOG_FILENAME = "website_scraper.log"
MEDIA_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
                    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                    '.zip', '.rar', '.7z', '.mp3', '.mp4', '.avi', '.mov', '.wmv',
                    '.flv', '.mpeg', '.mpg', '.webm', '.ogg', '.wav']

# --- Setup Logging ---
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_robot_parser(base_url):
    """Fetches and returns the RobotFileParser for the given base URL."""
    robot_url = urllib.parse.urljoin(base_url, 'robots.txt')
    rp = RobotFileParser()
    rp.set_url(robot_url)
    try:
        rp.read()
    except Exception as e:
        logging.warning(f"Error fetching or parsing robots.txt from {robot_url}: {e}")
        return None
    return rp

def is_allowed(url, base_url, robot_parser):
    """Checks if the URL is allowed to be scraped based on robots.txt."""
    if not robot_parser:
        return True  # If robots.txt parsing failed, assume allowed (or handle differently)
    return robot_parser.can_fetch('*', url)

def is_media_url(url):
    """Checks if the URL points to a media file based on its extension."""
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    for ext in MEDIA_EXTENSIONS:
        if path.lower().endswith(ext):
            return True
    return False

def fetch_page_content(url):
    """Fetches the content of a URL, handling potential errors and rate limiting."""
    try:
        time.sleep(DELAY_BETWEEN_REQUESTS)  # Rate limiting
        response = requests.get(url, headers={'User-Agent': 'WebsiteScraperBot/1.0'}) # Added User-Agent
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None

def extract_page_data(html_content, url):
    """Extracts page title, meta title, meta description, and links from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    page_title = soup.title.string.strip() if soup.title else "blank"
    meta_title_tag = soup.find("meta", attrs={"name": "title"}) or soup.find("meta", attrs={"property": "og:title"})
    meta_title = meta_title_tag["content"].strip() if meta_title_tag and meta_title_tag.has_attr('content') else "blank"
    meta_description_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description_tag["content"].strip() if meta_description_tag and meta_description_tag.has_attr('content') else "blank"

    links = []
    for link_tag in soup.find_all('a', href=True):
        link_url = link_tag.get('href')
        absolute_url = urllib.parse.urljoin(url, link_url) # Make relative URLs absolute
        if absolute_url.startswith(WEBSITE_URL) and not is_media_url(absolute_url): # Crawl only within website and not media files
            links.append(absolute_url)
    return {
        "Page Title": page_title,
        "Meta Title": meta_title,
        "Meta Description": meta_description,
        "Link": url  # Keeping original URL for output
    }, links

def scrape_website(base_url):
    """Crawls the website, extracts data, and saves to CSV."""
    start_time = datetime.datetime.now()
    logging.info(f"Starting website scrape for {base_url} at {start_time}")

    robot_parser = get_robot_parser(base_url)
    if robot_parser:
        logging.info("robots.txt fetched and parsed.")
    else:
        logging.warning("robots.txt not found or could not be parsed. Proceeding without robots.txt restrictions (be cautious!).")

    visited_urls = set()
    urls_to_visit = [base_url]
    output_data = []

    while urls_to_visit:
        current_url = urls_to_visit.pop(0) # FIFO for breadth-first-like crawling

        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)

        if not is_allowed(current_url, base_url, robot_parser):
            logging.info(f" robots.txt disallowed: Skipping {current_url}")
            continue

        logging.info(f" Crawling: {current_url}")
        html_content = fetch_page_content(current_url)
        if html_content:
            page_data, new_links = extract_page_data(html_content, current_url)
            output_data.append(page_data)
            for link in new_links:
                if link not in visited_urls and link not in urls_to_visit: # Avoid re-queuing already processed or queued URLs
                    urls_to_visit.append(link)
        else:
            logging.warning(f" Failed to fetch content for {current_url}")

    csv_filename = CSV_FILENAME.format(datetime.datetime.now().strftime("%Y-%m-%d"))
    save_to_csv(output_data, csv_filename)

    end_time = datetime.datetime.now()
    logging.info(f"Website scrape finished at {end_time}. Total time taken: {end_time - start_time}")
    logging.info(f"Data saved to {csv_filename}")


def save_to_csv(data, filename):
    """Saves the scraped data to a CSV file."""
    if not data:
        logging.info("No data to save to CSV.")
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Page Title", "Meta Title", "Meta Description", "Link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        logging.info(f"Successfully saved data to CSV file: {filename}")
    except Exception as e:
        logging.error(f"Error saving data to CSV file {filename}: {e}")


if __name__ == "__main__":
    if WEBSITE_URL == "YOUR_WEBSITE_URL_HERE":
        logging.error("Please replace 'YOUR_WEBSITE_URL_HERE' in the script with the actual website URL.")
        print("Error: Please configure the WEBSITE_URL in the script.") # To show error in console when run directly
    else:
        scrape_website(WEBSITE_URL)