import time
import random
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from utils import save_json, clean_text, ensure_directory_exists

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
        try:
            url = f"{self.base_url}?keywords={keywords}&location={location}"
            print(f"Searching: {url}")
            
            self.driver.get(url)
            time.sleep(5)
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            selectors = [
                "div.base-card.relative.w-full",
                "div[data-job-id]",
                ".job-card-container",
                ".jobs-search-results__list-item"
            ]
            
            cards = []
            for selector in selectors:
                try:
                    cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if cards:
                        print(f"Found {len(cards)} job cards using selector: {selector}")
                        break
                except:
                    continue
            
            if not cards:
                print("No job cards found with any selector")
                return 0
            
            for i, card in enumerate(cards[:max_jobs], 1):
                try:
                    title = self._safe_get_text(card, ["h3", "h4", ".job-title", "[data-test='job-title']"])
                    company = self._safe_get_text(card, ["h4", "h5", ".job-company", "[data-test='job-company']"])
                    location = self._safe_get_text(card, ["span", ".job-location", "[data-test='job-location']"])
                    
                    url_elem = card.find_element(By.TAG_NAME, "a")
                    job_url = url_elem.get_attribute("href").split('?')[0] if url_elem else ""
                    
                    if title and company:
                        job = {
                            'job_id': f"job_{i}_{int(time.time())}",
                            'title': title,
                            'company': company,
                            'location': location or "Not specified",
                            'source': 'LinkedIn',
                            'url': job_url,
                            'description': '',
                            'posted_date': ''
                        }
                        self.jobs.append(job)
                        print(f"  - {job['title']} at {job['company']}")
                    else:
                        print(f"  - Skipping job {i}: missing title or company")
                    
                except Exception as e:
                    print(f"Error on job {i}: {e}")
                    continue
            
            return len(self.jobs)
            
        except Exception as e:
            print(f"Search error: {e}")
            return 0
    
    def _safe_get_text(self, element, selectors):
        for selector in selectors:
            try:
                elem = element.find_element(By.CSS_SELECTOR, selector)
                text = elem.text.strip()
                if text:
                    return text
            except:
                continue
        return ""

    def save_jobs(self, filename: str = "jobs_raw.json"):
        if not self.jobs:
            print("No jobs to save")
            return
            
        ensure_directory_exists('data/raw')
        save_json(self.jobs, f"data/raw/{filename}")
        print(f"Saved {len(self.jobs)} jobs to data/raw/{filename}")

    def close(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    scraper = JobScraper()
    
    try:
        print("Searching for software engineering jobs...")
        job_count = scraper.search_jobs("software engineer", "United States", max_jobs=30)
        
        if job_count > 0:
            scraper.save_jobs("jobs_raw.json")
            print(f"\nSuccessfully collected {job_count} job postings!")
        else:
            print("No jobs found. Using test data instead.")
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from create_test_data import test_jobs
            ensure_directory_exists('data/raw')
            save_json(test_jobs, 'data/raw/jobs_raw.json')
            print("Test data saved to data/raw/jobs_raw.json")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Falling back to test data...")
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from create_test_data import test_jobs
            ensure_directory_exists('data/raw')
            save_json(test_jobs, 'data/raw/jobs_raw.json')
            print("Test data saved to data/raw/jobs_raw.json")
        except Exception as fallback_error:
            print(f"Failed to create test data: {fallback_error}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
