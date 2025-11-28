from bs4 import BeautifulSoup
import requests
import time
import json
from tqdm import tqdm

def get_all_starling_proto_dravidian():

    base_url = "https://starlingdb.org/cgi-bin/response.cgi"
    params = {
        "root": "config",
        "basename": "/data/drav/dravet",
        "first": 1  # increment by 20 for each page
    }

    entries = []

    for page in tqdm(range(111)):
        params["first"] = page * 20 + 1
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for record in soup.find_all('div', class_='results_record'):
            entry = {}
            for div in record.find_all('div', recursive=False):
                label_span = div.find('span', class_='fld')
                if label_span:
                    # Extract field name (strip colon and whitespace)
                    field_name = label_span.get_text(strip=True).rstrip(':')

                    if "Nostratic Etymology".lower() in field_name.lower(): 
                        #links to hypothetical nostratic etymology, not useful
                        continue

                    value_span = div.find('span', class_='unicode')
                    if value_span:
                        entry[field_name] = value_span.get_text(strip=True)
            
            if entry:
                entries.append(entry)
        
        time.sleep(1)

    return entries

def save_proto_dravidian_json(filepath):
    entries = get_all_starling_proto_dravidian()
    with open(filepath, 'w') as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)

save_proto_dravidian_json('proto_dravidian.json')