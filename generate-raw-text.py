import glob
import os
import json

PATH_INPUT            = "input"
PATH_OUTPUT           = "output"
PATH_POSTFIX_META     = "meta"
PATH_POSTFIX_DEEPGRAM = "deepgram"
PATH_TRANSCRIPT_RAW   = "transcript.raw"


def process_file(file_id: str):
    file_path_meta = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_META}.json")

    # Load meta data of the file
    meta = {}
    if os.path.exists(file_path_meta) == False:
        print(f"File {file_path_meta} does not exist")
        return
    with open(file_path_meta, 'r') as file:
        meta = json.load(file)

    # Process each language of the file
    for language in meta['languages']:
        file_path_deepgram       = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_POSTFIX_DEEPGRAM}.{language}.json")
        file_path_transcript_raw = os.path.join(PATH_OUTPUT, f"{file_id}.{PATH_TRANSCRIPT_RAW}.{language}.json")

        if os.path.exists(file_path_deepgram) == False:
            print(f"File {file_path_deepgram} does not exist")
            continue

        # Write transcript data
        with (
            open(file_path_deepgram, 'r')       as buffer_deepgram,
            open(file_path_transcript_raw, 'w') as buffer_transcript_output,
        ):
            data_deepgram = json.load(buffer_deepgram)
            # raw_text = data_deepgram["response"]["results"]["channels"][0]["alternatives"][0]["transcript"]
            # buffer_transcript_output.write(raw_text)

            raw_text = []
            paragraphs = data_deepgram["response"]["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
            for pidx, paragraph in enumerate(paragraphs):
                for sidx, sentence in enumerate(paragraph["sentences"]):
                    raw_text.append(f" {{{pidx}:{sidx}}} " + sentence["text"])

            buffer_transcript_output.writelines(raw_text)

def get_files_to_process(path: str) -> list[str]:
    meta_files = glob.glob(f"{path}*.deepgram.*.json", recursive=True)
    return [ os.path.basename(x)[:24] for x in meta_files ]


if __name__ == "__main__":
    files = get_files_to_process("output/")
    for file_id in files:
        process_file(file_id)
