import os
import json
import csv
from typing import Any, List, Dict, Union

def ensure_directory_exists(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)

def load_json(file_path: str) -> Union[Dict, List]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def save_json(data: Any, file_path: str) -> None:
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {len(data) if isinstance(data, list) else 1} records to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        raise

def save_csv(data: List[Dict[str, Any]], file_path: str) -> None:
    if not data:
        print("No data to save to CSV")
        return
        
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        fieldnames = set().union(*(d.keys() for d in data))
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(data)
        print(f"Successfully saved {len(data)} records to {file_path}")
    except Exception as e:
        print(f"Error saving CSV to {file_path}: {e}")
        raise

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return ' '.join(text.split())
