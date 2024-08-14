import glob
import os
import json
import requests
import concurrent.futures

# Define the path to the output folder
LIBRARY_VERSION   = "v0001"
URL_DATABASE      = "https://lectorium:lectorium@app.lectorium.akdasa.studio/database"
PATH_OUTPUT_DATA  = f"../../../content/library-{LIBRARY_VERSION}-data/"
PATH_OUTPUT_INDEX = f"../../../content/library-{LIBRARY_VERSION}-index/"


def save_file(
    database: str,
    file_path: str,
):
    with open(file_path, 'r') as file:
        data = json.load(file)
        _id = data.get('_id')
        url = f"{URL_DATABASE}/{database}/{_id}"
        response = requests.get(url)
        revision = None
        if response.status_code == 200:
            stored_data = response.json()
            revision = stored_data.get("_rev")
            saving_data = {**data, "_rev": revision}
            if stored_data == saving_data:
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
    all_files: list[tuple[str, str]] = []
    file_patterns = [
        (os.path.join(PATH_OUTPUT_DATA, "*.db.track.json"),         f"library-tracks-{LIBRARY_VERSION}"),
        (os.path.join(PATH_OUTPUT_DATA, "*.db.transcript.*.json"),  f"library-transcripts-{LIBRARY_VERSION}"),
        (os.path.join(PATH_OUTPUT_DATA, "*.db.author.json"),        f"library-dictionary-{LIBRARY_VERSION}"),
        (os.path.join(PATH_OUTPUT_DATA, "*.db.location.json"),      f"library-dictionary-{LIBRARY_VERSION}"),
        (os.path.join(PATH_OUTPUT_DATA, "*.db.source.json"),        f"library-dictionary-{LIBRARY_VERSION}"),
        (os.path.join(PATH_OUTPUT_INDEX, "*.db.index.json"),         f"library-index-{LIBRARY_VERSION}"),
    ]
    for pattern, database in file_patterns:
        files_found = glob.glob(pattern)
        all_files.extend([(file_name, database) for file_name in files_found])

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(
                save_file,
                file[1],
                file[0],
            ) for file in all_files
        ]

