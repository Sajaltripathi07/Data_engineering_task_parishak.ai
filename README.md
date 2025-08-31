# Job Data Processing Pipeline

A streamlined pipeline for processing job postings with cleaning and annotation capabilities.

## Project Structure
```
parishak.ai/
├── data/                  # Data storage
│   ├── raw/              # Raw job postings
│   ├── cleaned/          # Processed job data
│   └── annotated/        # Final annotated data
└── src/                  # Source code
    ├── scraper.py       # Simulates job posting data (dummy dataset generator)
    ├── cleaner.py       # Cleans raw job data
    ├── annotator.py     # Annotates processed data
    └── utils.py         # Utility functions
```

## Quick Start

1. Set up the environment:
   ```powershell
   # Create and activate virtual environment (Windows)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Install dependencies
   pip install -r requirements.txt
   ```

2. Run the pipeline:
   ```powershell
   # Process test data
   python src/cleaner.py
   python src/annotator.py
   ```

## Output
- Cleaned data: `data/cleaned/jobs_cleaned.json`
- Annotated data: `data/annotated/jobs_annotated.json`

## Notes
- The scraper currently uses test data. For production use, update `scraper.py` with actual job board APIs.
- Customize cleaning rules in `cleaner.py` as needed for your data.
- **Data Cleaning**: Removes duplicates, HTML tags, and normalizes text
- **Annotation**: Labels data with skills, experience level, and job type
