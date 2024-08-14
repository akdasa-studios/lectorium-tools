import glob
import os
import json

from sys import argv
import json

from modules.meta import AUTHORS, LOCATIONS, SOURCES

LIBRARY_VERSION = "v0001"
PATH_INPUT  = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else f"../../../content/library-{LIBRARY_VERSION}-data/"
PATH_POSTFIX_META          = "meta"
PATH_POSTFIX_META_URL      = "meta.url"
PATH_POSTFIX_DEEPGRAM      = "deepgram"
PATH_POSTFIX_DB_TRACK      = "db.track"
PATH_POSTFIX_DB_TRANSCRIPT = "db.transcript"
PATH_POSTFIX_DB_AUTHOR     = "db.author"
PATH_POSTFIX_DB_LOCATION   = "db.location"
PATH_POSTFIX_DB_SOURCE     = "db.source"


def process_file(
    file_id: str,
):
    # print(f"Processing {file_id}")
    file_path_meta              = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META}.json")
    file_path_meta_url          = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META_URL}.json")
    file_path_track_output      = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRACK}.json")

    # Load meta data of the file
    meta = {}
    if os.path.exists(file_path_meta) == False:
        print(f"File {file_path_meta} does not exist")
        return
    with open(file_path_meta, 'r') as file:
        meta = json.load(file)


    # Write track info data
    with (
        open(file_path_meta, 'r')         as buffer_meta,
        open(file_path_meta_url, 'r')     as buffer_meta_url,
        open(file_path_track_output, 'w') as buffer_track_output
    ):
        data_meta     = json.load(buffer_meta)
        data_meta_url = json.load(buffer_meta_url)
        data_track_output = {
            "_id":        f"{file_id}",
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
                "language": language,
                "source": "transcript",
                "type": "generated"
            } for language in data_meta["languages"]]
        }
        buffer_track_output.write(
            json.dumps(data_track_output, indent=2, ensure_ascii=False)
        )

    # Process each language of the file
    for language in meta['languages']:
        file_path_deepgram          = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DEEPGRAM}.{language}.json")
        file_path_transcript_output = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRANSCRIPT}.{language}.json")

        if os.path.exists(file_path_deepgram) == False:
            print(f"File {file_path_deepgram} does not exist")
            continue

        # Write transcript data
        with (
            open(file_path_deepgram, 'r')          as buffer_deepgram,
            open(file_path_transcript_output, 'w') as buffer_transcript_output,
        ):
            data_deepgram = json.load(buffer_deepgram)
            data_transcript_output   = {
                "_id": f"{file_id}::{data_deepgram["request"]["language"]}",
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
            buffer_transcript_output.write(
                json.dumps(data_transcript_output, indent=2, ensure_ascii=False)
            )


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

def get_files_to_process(path: str) -> list[str]:
    meta_files = glob.glob(f"{path}*.meta.json", recursive=True)
    return [ os.path.basename(x)[:24] for x in meta_files ]

if __name__ == "__main__":
    files = get_files_to_process(PATH_OUTPUT)
    for file_id in files:
        process_file(file_id)
    process_static_data()
