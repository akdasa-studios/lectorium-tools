import glob
import os
import json
import requests
import concurrent.futures

# Define the path to the output folder
PATH_OUTPUT = "output"


def save_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
        _id = data.get('_id')
        url = f"{URL_DATABASE}/library/{_id}"

        response = requests.get(url)
        revision = None
        if response.status_code == 200:
            stored_data = response.json()
            revision = stored_data.get("_rev")
            saving_data = {**data, "_rev": revision}
            if (stored_data == saving_data):
                print(f"Data for {_id} is up to date")
                return

        if revision is None:
            response = requests.put(url, json=data)
        else:
            response = requests.put(url, json={**data, "_rev": revision })

        if response.ok:
            print(f"Successfully updated data for {_id}")
        else:
            print(f"Failed to update data for {_id}: {response.text}")


if __name__ == "__main__":
    # get list of files to upload
    all_files = []
    file_patterns = [
        os.path.join(PATH_OUTPUT, "*.db.track.json"),
        os.path.join(PATH_OUTPUT, "*.db.transcript.*.json"),
        os.path.join(PATH_OUTPUT, "*.db.author.json"),
        os.path.join(PATH_OUTPUT, "*.db.location.json"),
        os.path.join(PATH_OUTPUT, "*.db.source.json"),
    ]
    for pattern in file_patterns:
        all_files.extend(glob.glob(pattern))

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(
                save_file,
                file,
            ) for file in all_files
        ]
