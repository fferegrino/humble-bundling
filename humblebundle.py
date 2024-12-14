import json
from collections import namedtuple
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from dict_functions import remove_empty_keys, remove_keys

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

Entry = namedtuple("Entry", ["query_time", "kind", "url", "content"])

query_time = datetime.now()
query_time_str = query_time.isoformat()


def load_js_data(page, script_id, extract_key=None):
    script_id = script_id.lstrip("/")
    page = requests.get(f"https://www.humblebundle.com/{page}")
    soup = BeautifulSoup(page.content, "html.parser")
    data = json.loads(soup.find("script", {"id": script_id}).text)
    if extract_key:
        data = data[extract_key]
    return data


all_bundles_data = load_js_data("bundles", "landingPage-json-data", "data")


entries = [Entry(query_time_str, "bundles", "/bundles", all_bundles_data)]

for kind in all_bundles_data.keys():
    for product in all_bundles_data[kind]["mosaic"][0]["products"]:
        product_data = load_js_data(product["product_url"], "webpack-bundle-page-data", "bundleData")
        product_data = remove_keys(
            product_data,
            [
                ["tier_item_data", "*", "front_page_art"],
                ["tier_item_data", "*", "resolved_paths"],
                ["tier_item_data", "*", "availability_icons"],
                ["charity_data", "charity_items", "*", "resolved_paths"],
                ["charity_data", "charity_items", "*", "front_page_art"],
                ["basic_data", "logo"],
                "other_bundles_data",
                "jplayer_swf_path",
                "tier_display_data",
                "leaderboard_data",
            ],
        )
        entries.append(Entry(query_time_str, kind, product["product_url"], product_data))

monthly_file = query_time.strftime("%Y-%m")


with open(data_dir / f"{monthly_file}.jsonl", "a") as f:
    for entry in entries:
        data_thing = remove_empty_keys(entry.content)
        data_thing["_ts"] = entry.query_time
        data_thing["_kind"] = entry.kind
        data_thing["_url"] = entry.url
        f.write(json.dumps(data_thing) + "\n")
