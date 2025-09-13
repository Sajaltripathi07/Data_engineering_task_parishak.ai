import json
from typing import Dict, List, Any
from utils import load_json, save_json, save_csv

class JobAnnotator:
    def __init__(self):
        self.experience_levels = {
            'Entry': ['entry', 'fresher', '0-1', '0-2', 'junior'],
            'Mid': ['mid', '2-4', '3-5', 'intermediate'],
            'Senior': ['senior', 'lead', '5+', '5+ years'],
            'Executive': ['manager', 'director', 'vp', 'cto']
        }
        
        self.job_keywords = {
            'Backend': ['backend', 'api', 'server', 'database', 'sql', 'nosql'],
            'Frontend': ['frontend', 'react', 'angular', 'vue', 'javascript'],
            'Fullstack': ['full stack', 'full-stack', 'mern', 'mean'],
            'DevOps': ['devops', 'aws', 'azure', 'docker', 'kubernetes'],
            'Data': ['data science', 'machine learning', 'ai', 'data analysis'],
            'Mobile': ['ios', 'android', 'react native', 'flutter'],
            'QA': ['qa', 'testing', 'test automation', 'selenium']
        }
        
        self.education_levels = {
            'No Degree': ['no degree', 'high school', 'diploma'],
            'Bachelor\'s': ['bachelor', 'b.tech', 'b.e.', 'bsc', 'bs '],
            'Master\'s': ['master', 'msc', 'm.tech', 'mba'],
            'PhD': ['phd', 'doctorate']
        }

    def get_experience(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return 'Not specified'
        text = text.lower()
        for level, keywords in self.experience_levels.items():
            if any(keyword in text for keyword in keywords):
                return level
        return 'Mid'
    
    def get_job_type(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return 'Not specified'
        text = text.lower()
        for job_type, keywords in self.job_keywords.items():
            if any(keyword in text for keyword in keywords):
                return job_type
        return 'Other'
    
    def get_education(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return 'Not specified'
        text = text.lower()
        if 'phd' in text or 'doctorate' in text:
            return 'PhD'
        if 'master' in text or 'msc' in text or 'mba' in text:
            return 'Master\'s'
        return 'Bachelor\'s'
    
    def get_salary(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return 'Not specified'
        text = text.lower()
        if 'lpa' in text or 'lakh' in text:
            return 'Competitive'
        return 'Not specified'
    
    def annotate_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        try:
            text = f"{job.get('title', '')} {job.get('description', '')}"
            
            job['experience'] = self.get_experience(text)
            job['job_type'] = self.get_job_type(text)
            job['education'] = self.get_education(text)
            job['salary'] = self.get_salary(text)
            
            return job
            
        except Exception as e:
            print(f"Error with job {job.get('job_id', 'unknown')}")
            return None
    
    def process_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [job for job in (self.annotate_job(j) for j in jobs) if job]

def main():
    try:
        jobs = load_json('data/cleaned/jobs_cleaned.json')
        print(f"Loaded {len(jobs)} jobs")
        
        annotator = JobAnnotator()
        annotated_jobs = annotator.process_jobs(jobs)
        
        save_json(annotated_jobs, 'data/annotated/jobs_annotated.json')
        save_csv(annotated_jobs, 'data/annotated/jobs_annotated.csv')
        
        if annotated_jobs:
            print("\nSample job:")
            job = annotated_jobs[0]
            print(f"Title: {job.get('title')}")
            print(f"Type: {job.get('job_type')}")
            print(f"Experience: {job.get('experience')}")
            print(f"Education: {job.get('education')}")
            print(f"Salary: {job.get('salary')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
