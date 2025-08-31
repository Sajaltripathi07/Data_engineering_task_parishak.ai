import time
import random
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils import save_to_json, clean_text, ensure_directory_exists

class JobScraper:
    def __init__(self, headless=True):
        self.base_url = "https://www.linkedin.com/jobs/search/"
        self.jobs = []
        self.setup_driver(headless)

    def setup_driver(self, headless):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        if headless:
            options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(20)

    def search_jobs(self, keywords: str, location: str, max_jobs: int = 10) -> int:
        """Search for jobs with basic info only"""
        try:
            url = f"{self.base_url}?keywords={keywords}&location={location}"
            print(f"Searching: {url}")
            
            self.driver.get(url)
            time.sleep(3)  # Simple wait for page load
            
            # Scroll to load jobs
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Get job cards
            cards = self.driver.find_elements(By.CSS_SELECTOR, 
                "div.base-card.relative.w-full")
            
            print(f"Found {len(cards)} job cards")
            
            # Extract basic job info
            for i, card in enumerate(cards[:max_jobs], 1):
                try:
                    job = {
                        'job_id': f"job_{i}_{int(time.time())}",
                        'title': card.find_element(By.CSS_SELECTOR, "h3").text.strip(),
                        'company': card.find_element(By.CSS_SELECTOR, "h4").text.strip(),
                        'location': card.find_element(By.CSS_SELECTOR, "span").text.strip(),
                        'source': 'LinkedIn',
                        'url': card.find_element(By.TAG_NAME, "a").get_attribute("href").split('?')[0]
                    }
                    self.jobs.append(job)
                    print(f"  - {job['title']} at {job['company']}")
                    
                except Exception as e:
                    print(f"Error on job {i}: {e}")
                    continue
            
            return len(self.jobs)
            
        except Exception as e:
            print(f"Search error: {e}")
            return 0

    def save_jobs(self, filename: str = "jobs_raw.json"):
        """Save jobs to file"""
        if not self.jobs:
            print("No jobs to save")
            return
            
        ensure_directory_exists('data/raw')
        save_to_json(self.jobs, f"data/raw/{filename}")
        print(f"Saved {len(self.jobs)} jobs to data/raw/{filename}")

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    scraper = JobScraper()
    
    try:
        # Scrape from both sources
        linkedin_jobs = scraper.scrape_linkedin_jobs(count=30)
        indeed_jobs = scraper.scrape_indeed_jobs(count=20)
        
        # Combine and save results
        all_jobs = linkedin_jobs + indeed_jobs
        
        # Ensure data directory exists
        ensure_directory_exists('data/raw')
        
        # Save raw data
        save_to_json(all_jobs, 'data/raw/jobs_raw.json')
        print(f"\nSuccessfully collected {len(all_jobs)} job postings!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
