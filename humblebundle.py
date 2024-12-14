import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from collections import namedtuple
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

Entry = namedtuple('Entry', ['query_time','kind', 'url','content'])

query_time = datetime.now()
query_time_str = query_time.isoformat()

def load_js_data(page, script_id, extract_key=None):
    script_id = script_id.lstrip("/")
    page = requests.get(f"https://www.humblebundle.com/{page}")
    soup = BeautifulSoup(page.content, "html.parser")
    data = json.loads(soup.find('script', {'id':script_id}).text)
    if extract_key:
        data = data[extract_key]
    return data

all_bundles_data = load_js_data("bundles", "landingPage-json-data", 'data')

all_bundles_data['data'].keys()

entries = [
    Entry(query_time_str, 'bundles', '/bundles', json.dumps(all_bundles_data))
]

for kind in all_bundles_data['data'].keys():
    for product in all_bundles_data['data'][kind]['mosaic'][0]['products']:
        product_data = load_js_data(product['product_url'], 'webpack-bundle-page-data', 'bundleData')
        entries.append(Entry(query_time_str, kind, product['product_url'], json.dumps(product_data)))

monthly_file = query_time.strftime("%Y-%m")

def remove_empty_keys(data):
    empty_keys = []
    for key, value in data.items():
        if value is None:
            empty_keys.append(key)
        elif isinstance(value, dict):
            remove_empty_keys(value)
            if not value:
                empty_keys.append(key)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    remove_empty_keys(item)
                    if not item:
                        empty_keys.append(key)
                elif isinstance(item, str):
                    if not item:
                        empty_keys.append(key)
    for key in empty_keys:
        del data[key]
    return data

with open(data_dir / f"{monthly_file}.jsonl", "a") as f:
    for entry in entries:
        data_thing = remove_empty_keys(entry.content)
        data_thing['_ts'] = entry.query_time
        data_thing['_kind'] = entry.kind
        data_thing['_url'] = entry.url
        f.write(json.dumps(data_thing) + "\n")

