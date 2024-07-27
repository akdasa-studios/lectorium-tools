import glob
import os
import json
import requests

# Define the path to the output folder
PATH_OUTPUT = "output"
URL_DATABASE = "http://lectorium:lectorium@database:5984"

file_patterns = [
    os.path.join(PATH_OUTPUT, "*.db.track.json"),
    os.path.join(PATH_OUTPUT, "*.db.transcript.*.json")
]

all_files = []
for pattern in file_patterns:
    all_files.extend(glob.glob(pattern))


for file_path in all_files:
    with open(file_path, 'r') as file:
        data = json.load(file)
        _id = data.get('_id').replace("/", "%2F")
        url = f"{URL_DATABASE}/library/{_id}"

        response = requests.get(url)
        revision = None
        if response.status_code == 200:
            stored_data = response.json()
            revision = stored_data.get("_rev")
            saving_data = {**data, "_rev": revision}
            if (stored_data == saving_data):
                print(f"Data for {_id} is up to date")
                continue

        if revision is None:
            response = requests.put(url, json=data)
        else:
            response = requests.put(url, json={**data, "_rev": revision })

        if response.ok:
            print(f"Successfully updated data for {_id}")
        else:
            print(f"Failed to update data for {_id}: {response.text}")
