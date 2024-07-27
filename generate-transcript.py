import os
import json

from sys import argv
from db import LANGUAGES
from deepgram import DeepgramClient, PrerecordedOptions, PrerecordedResponse

# The API key we created in step 3
DEEPGRAM_API_KEY = 'b3a88047ed33bc30ad20ca808ecc25eeac9c422e'

PATH_INPUT = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"
PATH_POSTFIX = "deepgram"

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

# ----------------
# Helper functions
# ----------------

def get_file_id(
    path: str,
) -> str:
    """
    Extract file ID from the file path.
    """
    file_name = os.path.basename(path)
    return file_name.split(" ")[0]

def get_language_from_path(
    path: str,
) -> str:
    """
    Extract language from the file path.
    """
    folders = os.path.dirname(path).split("/")
    for language in LANGUAGES:
        canonical_name = language[0]
        for folder in folders:
            if folder.lower() == canonical_name.lower():
                return canonical_name
    raise Exception(f"Language not found in path {path}")

# --------------------
# Processing functions
# --------------------

def save_result(
    path: str,
    request: dict,
    response: dict,
):
    """
    Save the result to the output directory in JSON format with the given path.
    """
    with open(path, 'w') as output_file:
        output_file.write(json.dumps({
            'request': request,
            'response': response
        }, indent=4, ensure_ascii=False))


def process_file(
    path: str,
    language: str,
):
    """
    Process a single file and save the output to the output directory.
    """
    print(f"Processing {path} in {language}")

    with open(path, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }
        options = PrerecordedOptions(
            language=language,
            smart_format=True,
            model="nova-2",
            paragraphs=True
        )
        response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
        return response.to_dict()

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
            file_id = get_file_id(item_full_path)
            output_path = f"{PATH_OUTPUT}/{file_id}.{PATH_POSTFIX}.json"
            if os.path.exists(output_path):
                print(f"File {output_path} already exists")
                continue

            language = get_language_from_path(item_full_path)
            response = process_file(item_full_path, language)
            save_result(
                path=output_path,
                request={ "language": language },
                response=response
            )

if __name__ == "__main__":
    process_dir(PATH_INPUT)
