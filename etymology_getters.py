from bs4 import BeautifulSoup
import requests
import time
import json
import re
from tqdm import tqdm

BASE_URL = "https://starlingdb.org/cgi-bin/"

def exponential_retry(url, max_retries=20, **kwargs):
    """Perform GET request with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def extract_subquery_url(onclick_attr):
    """Extract the subquery URL from an onclick attribute."""
    match = re.search(r"subquery\(this,'([^']+)'\)", onclick_attr)
    if match:
        return BASE_URL + match.group(1).replace('&amp;', '&')
    return None

def parse_record(record, fetch_subqueries=True):
    """Parse a results_record div into a dictionary."""
    entry = {}
    
    for div in record.find_all('div', recursive=False):
        label_span = div.find('span', class_='fld')
        if not label_span:
            continue
        
        field_name = label_span.get_text(strip=True).rstrip(':')
        
        if "etymology" in field_name.lower(): #removes dravidian etymology back-links, nostratic etymology
            continue

        value_span = div.find('span', class_='unicode')
        field_value = value_span.get_text(strip=True) if value_span else None
        
        # Check for subquery
        subquery_data = None
        if fetch_subqueries:
            img = div.find('img', class_='plus', onclick=True)
            if img:
                subquery_url = extract_subquery_url(img.get('onclick'))
                if subquery_url:
                    subquery_data = fetch_subquery(subquery_url)
                    time.sleep(0.3)
        
        if subquery_data:
            entry[field_name] = subquery_data
        elif field_value:
            entry[field_name] = field_value
    
    return entry

def fetch_subquery(url):
    """Fetch a subquery URL and parse its record."""
    try:
        response = exponential_retry(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        record = soup.find('div', class_='results_record')
        if record:
            return parse_record(record, fetch_subqueries=True)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def get_all_starling_proto_dravidian():
    base_url = "https://starlingdb.org/cgi-bin/response.cgi"
    params = {
        "root": "config",
        "basename": "/data/drav/dravet",
        "first": 1
    }

    entries = []

    for page in tqdm(range(111)):
        params["first"] = page * 20 + 1
        response = exponential_retry(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for record in tqdm(soup.find_all('div', class_='results_record')):
            entry = parse_record(record, fetch_subqueries=True)
            if entry:
                entries.append(entry)
        
        time.sleep(0.3)

    return entries

def save_proto_dravidian_json(filepath):
    entries = get_all_starling_proto_dravidian()
    with open(filepath, 'w') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

save_proto_dravidian_json('full_proto_dravidian.json')