import glob
import os
import json
import concurrent.futures

from sys import argv
from deepgram import DeepgramClient, PrerecordedOptions


# The API key we created in step 3
PATH_INPUT = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"
PATH_POSTFIX = "deepgram"

deepgram = DeepgramClient(DEEPGRAM_API_KEY)


def process_file(
    file_id: str,
):
    file_path_meta       = f"{PATH_OUTPUT}/{file_id}.meta.json"
    file_path_transcript = f"{PATH_OUTPUT}/{file_id}.{PATH_POSTFIX}.json"

    # Load meta data
    meta = {}
    with open(file_path_meta, 'r') as file:
        meta = json.load(file)

    # Process each language
    for language in meta['languages']:
        print(f"Processing {meta['id']} in {language}: {meta['path']}")
        with open(meta['path'], 'rb') as buffer_data:
            payload = { 'buffer': buffer_data }
            options = PrerecordedOptions(
                language=language,
                smart_format=True,
                model="nova-2",
                paragraphs=True
            )
            response = deepgram.listen.rest.v('1').transcribe_file(payload, options)

            with open(file_path_transcript, 'w') as output_file:
                output_file.write(json.dumps({
                    'request': { "language": language },
                    'response': response.to_dict()
                }, indent=2, ensure_ascii=False))

def get_files_to_process(path: str) -> list[str]:
    """
    Get list of file ids that need to be processed.
    """
    meta_files       = glob.glob(f"{path}*.meta.json", recursive=True)
    transcript_files = glob.glob(f"{path}*.deepgram.json", recursive=True)
    meta_ids         = { os.path.basename(x)[:24] for x in meta_files }
    transcript_ids   = { os.path.basename(x)[:24] for x in transcript_files }

    return list(meta_ids - transcript_ids)

if __name__ == "__main__":
    files_ids = get_files_to_process("output/")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(
                process_file,
                file_id,
            ) for file_id in files_ids
        ]
