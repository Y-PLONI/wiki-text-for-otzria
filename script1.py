import os
import json
import requests
import time
import random
import urllib.parse
import re

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

def clean_filename(filename):
    return re.sub(r'[":,/\[\]]', '', filename)

def clean_filenames_list(filenames):
    return [re.sub(r'[":,/\[\]]', '', filename) for filename in filenames]

def download_file(url, dest_folder, filename):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        file_path = os.path.join(dest_folder, f"{filename}.htmlz")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved to {file_path}")
    else:
        print(f"Failed to download {url}")

def process_json(json_data, base_folder, parent_keys=[]):
    for key, value in json_data.items():
        current_keys = clean_filenames_list(parent_keys) + [clean_filename(key)]
        if isinstance(value, dict) and value:
            process_json(value, base_folder, current_keys)
        else:
            dest_folder = os.path.join(base_folder, *current_keys[:-1])
            filename = current_keys[-1]
            encoded_filename = urllib.parse.quote(filename)
            url = f"https://ws-export.wmcloud.org/?lang=he&page={encoded_filename}&format=htmlz&fonts=&credits=false&images=false"
            download_file(url, dest_folder, clean_filename(filename))
            delay = random.randint(30, 35)
            print(f"Waiting for {delay} seconds...")
            time.sleep(delay)

def main():
    json_file_path = 'data.json'  # Path to your JSON file
    base_folder = 'ארון הספרים היהודי'  # Root folder for downloads

    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    process_json(json_data, base_folder)

if __name__ == "__main__":
    main()
