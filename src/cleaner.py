import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import List, Dict, Any

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from utils import load_json, save_json, save_csv

class DataCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'aws', 'react',
            'docker', 'kubernetes', 'html', 'css', 'node.js', 'git', 'github'
        ]
        self.job_stopwords = {
            'applicant', 'applicants', 'required', 'requirements',
            'ability', 'abilities', 'work', 'working', 'job', 'position',
            'role', 'responsibilities', 'duties', 'tasks'
        }
        self.stop_words = self.stop_words - self.job_stopwords

    def clean_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
            
        text = text.lower()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens 
                 if t not in self.stop_words and len(t) > 2]
        
        return ' '.join(tokens)

    def get_skills(self, text: str) -> str:
        if not text:
            return ""
        found = [s for s in self.skills if s in text.lower()]
        return ', '.join(found) if found else "Not specified"

    def clean_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not job.get('job_id'):
                print("Skipping job: missing job_id")
                return None
                
            job['title'] = self.clean_text(job.get('title', ''))
            job['description'] = self.clean_text(job.get('description', ''))
            job['company'] = self.clean_text(job.get('company', ''))
            job['location'] = self.clean_text(job.get('location', ''))
            
            if not job['title'] and not job['company']:
                print(f"Skipping job {job.get('job_id', 'unknown')}: missing title and company")
                return None
            
            job['skills'] = self.get_skills(job['description'])
            
            original_desc = job.get('description', '')
            if isinstance(original_desc, str):
                job['raw_description'] = original_desc[:500]
            else:
                job['raw_description'] = str(original_desc)[:500]
            
            return job
            
        except Exception as e:
            print(f"Error with job {job.get('job_id', 'unknown')}: {e}")
            return None

    def process_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [job for job in (self.clean_job(j) for j in jobs) if job]


def main():
    try:
        cleaner = DataCleaner()
        
        input_files = [
            'data/raw/jobs_raw.json',
            'data/raw/test_jobs.json'
        ]
        
        all_jobs = []
        
        for input_file in input_files:
            try:
                print(f"Processing {input_file.split('/')[-1]}...")
                jobs = load_json(input_file)
                cleaned = cleaner.process_jobs(jobs)
                print(f"Cleaned: {len(cleaned)} jobs")
                all_jobs.extend(cleaned)
                
            except Exception as e:
                print(f"Skipping {input_file}: {str(e)}")
        
        if not all_jobs:
            print("No valid jobs found")
            return
        
        save_json(all_jobs, 'data/cleaned/jobs_cleaned.json')
        save_csv(all_jobs, 'data/cleaned/jobs_cleaned.csv')
        
        print(f"\nSaved {len(all_jobs)} jobs to data/cleaned/")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
