from os import listdir, path
from sys import argv
import json

PATH_INPUT  = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"
PATH_POSTFIX_META          = "meta"
PATH_POSTFIX_DEEPGRAM      = "deepgram"
PATH_POSTFIX_DB_TRACK      = "db.track"
PATH_POSTFIX_DB_TRANSCRIPT = "db.transcript"


for file_name in listdir(PATH_INPUT):
    print(f"Processing {file_name}")
    file_id                     = file_name.split(" ")[0]
    file_path_meta              = path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META}.json")
    file_path_deepgram          = path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DEEPGRAM}.json")
    file_path_track_output      = path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRACK}.json")
    file_path_transcript_output = path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DB_TRANSCRIPT}.json")

    with (
        open(file_path_meta, 'r')              as buffer_meta,
        open(file_path_deepgram, 'r')          as buffer_deepgram,
        open(file_path_track_output, 'w')      as buffer_track_output,
        open(file_path_transcript_output, 'w') as buffer_transcript_output,
    ):
        data_meta     = json.load(buffer_meta)
        data_deepgram = json.load(buffer_deepgram)
        data_track_output   = {
            "_id": f"track/{file_id}/info",
            "title": data_meta["title"],
            "location": data_meta["location"],
            "date": data_meta["date"],
            "references": data_meta["references"],
        }
        data_transcript_output   = {
            "_id": f"track/{file_id}/transcript",
            "text": {
                "paragraphs": []
            }
        }

        # extract data from source files
        paragraphs = data_deepgram["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
        for paragraph in paragraphs:
            data_transcript_output["text"]["paragraphs"].append(paragraph["sentences"])

        # Write to output files
        buffer_track_output.write(
            json.dumps(data_track_output, indent=4, ensure_ascii=False)
        )
        buffer_transcript_output.write(
            json.dumps(data_transcript_output, indent=4, ensure_ascii=False)
        )


    break
