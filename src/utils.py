import os
import json
import csv
from typing import Any, List, Dict, Union

def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)

def load_json(file_path: str) -> Union[Dict, List]:
    """Load JSON data from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Any, file_path: str) -> None:
    """Save data to JSON file"""
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_csv(data: List[Dict[str, Any]], file_path: str) -> None:
    """Save list of dicts to CSV"""
    if not data:
        return
        
    ensure_directory_exists(os.path.dirname(file_path))
    fieldnames = set().union(*(d.keys() for d in data))
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
        writer.writeheader()
        writer.writerows(data)

def clean_text(text: str) -> str:
    """Basic text cleaning"""
    if not isinstance(text, str):
        return ""
    return ' '.join(text.split())
