import json
import random
from datetime import datetime, timedelta

# Sample job data
titles = ["Software Engineer", "Data Scientist", "Frontend Developer", "DevOps Engineer", "Backend Developer"]
companies = ["TechCorp", "DataSystems", "WebSolutions", "CloudTech", "AI Innovations"]
descriptions = [
    "Looking for a skilled software engineer with experience in Python and web development.",
    "Join our data science team to work on cutting-edge machine learning projects.",
    "Frontend developer needed with React and TypeScript experience.",
    "DevOps engineer to manage our cloud infrastructure and CI/CD pipelines.",
    "Backend developer with expertise in Node.js and databases."
]

# Generate test data
test_jobs = []
for i in range(10):
    job = {
        "job_id": f"job_{i+1000}",
        "title": random.choice(titles),
        "company": random.choice(companies),
        "location": f"City {random.randint(1, 5)}",
        "description": random.choice(descriptions),
        "posted_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
        "url": f"https://example.com/job/{i+1000}",
        "source": random.choice(["LinkedIn", "Indeed"])
    }
    test_jobs.append(job)

# Save to file
with open('data/raw/test_jobs.json', 'w') as f:
    json.dump(test_jobs, f, indent=2)

print("Test data created at data/raw/test_jobs.json")
