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
    ├── scraper.py       # Web scraper for job postings
    ├── cleaner.py       # Data cleaning module
    ├── annotator.py     # Job annotation module
    └── utils.py         # Utility functions
```

## How to Run the Project

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed (for web scraping)
- ChromeDriver (automatically managed by Selenium)

### 1. Environment Setup

```powershell
# Create and activate virtual environment (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Complete Pipeline

#### Option A: Full Pipeline (Recommended)
```powershell
# Step 1: Generate test data (optional - creates sample job postings)
python create_test_data.py

# Step 2: Run the scraper (attempts LinkedIn scraping, falls back to test data)
python src/scraper.py

# Step 3: Clean the data
python src/cleaner.py

# Step 4: Annotate the data
python src/annotator.py
```

#### Option B: Individual Components
```powershell
# Only run data cleaning (requires existing raw data)
python src/cleaner.py

# Only run annotation (requires existing cleaned data)
python src/annotator.py

# Only run scraper (will create raw data)
python src/scraper.py
```

### 3. Expected Output

After running the complete pipeline, you should see:
- **Raw data**: `data/raw/jobs_raw.json` (scraped or test data)
- **Cleaned data**: `data/cleaned/jobs_cleaned.json` and `jobs_cleaned.csv`
- **Annotated data**: `data/annotated/jobs_annotated.json` and `jobs_annotated.csv`

### 4. Troubleshooting

- **If scraper fails**: The system automatically falls back to test data
- **If no jobs are processed**: Check that input files exist in `data/raw/`
- **Chrome/WebDriver issues**: Ensure Chrome browser is installed and up-to-date

## Features

- **Web Scraping**: Automated job posting collection from LinkedIn (with fallback to test data)
- **Data Cleaning**: Removes HTML tags, normalizes text, and extracts skills
- **Job Annotation**: Automatically categorizes jobs by type, experience level, and education requirements
- **Multiple Output Formats**: JSON and CSV export options
- **Error Handling**: Robust error handling with graceful fallbacks
- **Data Validation**: Ensures data quality at each processing stage

## Notes
- The scraper attempts real LinkedIn scraping but falls back to test data if scraping fails
- For production use, consider using official job board APIs instead of web scraping
- Customize cleaning rules in `cleaner.py` and annotation logic in `annotator.py` as needed
- All data processing includes comprehensive error handling and validation
