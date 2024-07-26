from os import listdir, path
from sys import argv
from deepgram import DeepgramClient, PrerecordedOptions

# The API key we created in step 3
DEEPGRAM_API_KEY = 'b3a88047ed33bc30ad20ca808ecc25eeac9c422e'

PATH_INPUT = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"
PATH_POSTFIX = "deepgram"

deepgram = DeepgramClient(DEEPGRAM_API_KEY)

for file_name in listdir(PATH_INPUT):
    print(f"Processing {file_name}")
    file_id = file_name.split(" ")[0]
    file_path = path.join(PATH_INPUT, file_name)

    with open(file_path, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }

        options = PrerecordedOptions(
            smart_format=True, model="nova-2",
            language="ru",
            paragraphs=True
        )
        response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)

        output_path = f"{PATH_OUTPUT}/{file_id}.{PATH_POSTFIX}.json"
        file_data   = response.to_json(indent=4, ensure_ascii=False)
        with open(output_path, 'w') as output_file:
            output_file.write(file_data)

    break
