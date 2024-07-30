import os
import json

from sys import argv
import json

from modules.meta import extract_id, AUTHORS, LOCATIONS, SOURCES

PATH_INPUT  = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"
PATH_POSTFIX_META          = "meta"
PATH_POSTFIX_META_URL      = "meta.url"
PATH_POSTFIX_DEEPGRAM      = "deepgram"
PATH_POSTFIX_DB_TRACK      = "db.track"
PATH_POSTFIX_DB_TRANSCRIPT = "db.transcript"
PATH_POSTFIX_DB_AUTHOR     = "db.author"
PATH_POSTFIX_DB_LOCATION   = "db.location"
PATH_POSTFIX_DB_SOURCE     = "db.source"

# ----------------
# Helper functions
# ----------------

def get_language_from_deepgram_response(
    path: str,
) -> str:
    with open(path, 'r') as buffer_deepgram:
        data_deepgram = json.load(buffer_deepgram)
        return data_deepgram["request"]["language"]


# --------------------
# Processing functions
# --------------------

def process_file(
    path: str,
):
    print(f"Processing {path}")
    file_id                     = extract_id(path)
    file_path_meta              = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META}.json")
    file_path_meta_url          = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META_URL}.json")
    file_path_deepgram          = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DEEPGRAM}.json")
    file_path_track_output      = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRACK}.json")
    file_path_transcript_output = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRANSCRIPT}.{get_language_from_deepgram_response(file_path_deepgram)}.json")

    if os.path.exists(file_path_meta) == False:
        print(f"File {file_path_meta} does not exist")
        return
    if os.path.exists(file_path_deepgram) == False:
        print(f"File {file_path_deepgram} does not exist")
        return

    with (
        open(file_path_meta, 'r')              as buffer_meta,
        open(file_path_meta_url, 'r')          as buffer_meta_url,
        open(file_path_deepgram, 'r')          as buffer_deepgram,
        open(file_path_track_output, 'w')      as buffer_track_output,
        open(file_path_transcript_output, 'w') as buffer_transcript_output,
    ):
        data_meta     = json.load(buffer_meta)
        data_meta_url = json.load(buffer_meta_url)
        data_deepgram = json.load(buffer_deepgram)
        data_track_output = {
            "_id":        f"track::{file_id}::info",
            "url":        data_meta_url["url"],
            "title":      data_meta["title"],
            "location":   data_meta["location"],
            "date":       data_meta["date"],
            "file_size":  data_meta["file_size"],
            "duration":   data_meta["duration"],
            "author":     data_meta["author"],
            "references": data_meta["references"],
            "languages":  [{
                "language": language,
                "source": "track",
                "type": "original"
            } for language in data_meta["languages"]] + [{
                "language": data_deepgram["request"]["language"],
                "source": "transcript",
                "type": "generated"
            }]
        }
        data_transcript_output   = {
            "_id": f"track::{file_id}::transcript::{data_deepgram["request"]["language"]}",
            "text": {
                "blocks": []
            }
        }

        # extract data from transcript file
        paragraphs = data_deepgram["response"]["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
        for paragraph in paragraphs:
            for sentence in paragraph["sentences"]:
                data_transcript_output["text"]["blocks"].append({
                    "type": "sentence",
                    "text": sentence["text"],
                    "start": sentence["start"],
                    "end": sentence["end"],
                })
            data_transcript_output["text"]["blocks"].append({
                "type": "paragraph",
            })

        # Write to output files
        buffer_track_output.write(
            json.dumps(data_track_output, indent=2, ensure_ascii=False)
        )
        buffer_transcript_output.write(
            json.dumps(data_transcript_output, indent=2, ensure_ascii=False)
        )

def process_dir(
    path: str,
):
    """
    Process all files in the directory and subdirectories.
    """
    for item in os.listdir(path):
        item_full_path = os.path.join(path, item)
        if os.path.isdir(item_full_path):
            process_dir(item_full_path)
        else:
            process_file(item_full_path)

def process_static_data():
    for author in AUTHORS:
        file_author_output = os.path.join(PATH_OUTPUT, f"author.{author.code}.{PATH_POSTFIX_DB_AUTHOR}.json")
        with open(file_author_output, 'w') as buffer_author_output:
            data_author_output = {
                "_id": f"author::{author.code}",
                "name": {
                    language: name
                    for language, name in author.canonical_names.items()
                },
            }
            buffer_author_output.write(
                json.dumps(data_author_output, indent=2, ensure_ascii=False)
            )

    for location in LOCATIONS:
        file_location_output = os.path.join(PATH_OUTPUT, f"location.{location.code}.{PATH_POSTFIX_DB_LOCATION}.json")
        with open(file_location_output, 'w') as buffer_location_output:
            data_location_output = {
                "_id": f"location::{location.code}",
                "name": {
                    language: name
                    for language, name in location.canonical_names.items()
                },
            }
            buffer_location_output.write(
                json.dumps(data_location_output, indent=2, ensure_ascii=False)
            )

    for source in SOURCES:
        file_source_output = os.path.join(PATH_OUTPUT, f"source.{source.code}.{PATH_POSTFIX_DB_SOURCE}.json")
        with open(file_source_output, 'w') as buffer_source_output:
            data_source_output = {
                "_id": f"source::{source.code}",
                "name": {
                    language: name
                    for language, name in source.canonical_names.items()
                },
            }
            buffer_source_output.write(
                json.dumps(data_source_output, indent=2, ensure_ascii=False)
            )

if __name__ == "__main__":
    process_dir(PATH_INPUT)
    process_static_data()
