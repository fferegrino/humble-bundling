import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from collections import namedtuple
import csv
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

Entry = namedtuple('Entry', ['query_time','kind', 'url','content'])

query_time = datetime.now()
query_time_str = query_time.isoformat()

def load_js_data(page, script_id):
    script_id = script_id.lstrip("/")
    page = requests.get(f"https://www.humblebundle.com/{page}")
    soup = BeautifulSoup(page.content, "html.parser")
    data = json.loads(soup.find('script', {'id':script_id}).text)
    return data

all_bundles_data = load_js_data("bundles", "landingPage-json-data")

all_bundles_data['data'].keys()

entries = [
    Entry(query_time_str, 'bundles', '/bundles', json.dumps(all_bundles_data))
]

for kind in all_bundles_data['data'].keys():
    for product in all_bundles_data['data'][kind]['mosaic'][0]['products']:
        product_data = load_js_data(product['product_url'], 'webpack-bundle-page-data')
        entries.append(Entry(query_time_str, kind, product['product_url'], json.dumps(product_data)))

monthly_file = query_time.strftime("%Y-%m")
monthly_file

with open(data_dir / f"{monthly_file}.csv", "a") as f:
    writer = csv.writer(f)
    for entry in entries:
        writer.writerow(entry)

