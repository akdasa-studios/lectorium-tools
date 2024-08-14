import datetime
import glob
import json

from nltk.stem.snowball import SnowballStemmer
from nltk import download
from nltk.tokenize import word_tokenize

LIBRARY_VERSION = "v0001"
INPUT_PATH      = f"../../../../content/library-{LIBRARY_VERSION}-data/"
OUTPUT_PATH     = f"../../../../content/library-{LIBRARY_VERSION}-index"
download('punkt')


def get_file_paths_to_process():
    return glob.glob(f"{INPUT_PATH}/**/*.meta.json", recursive=True)


def get_file_id(file_path: str):
    with open(file_path, 'r') as meta_buffer:
        meta_json = json.load(meta_buffer)
        return meta_json["id"]


def get_content_to_index(file_path: str):
    with open(file_path, 'r') as meta_buffer:
        meta_json = json.load(meta_buffer)
        references = meta_json["references"]
        references = [ref[0] + " " + " ".join(map(str, ref[1:])) for ref in references]
        date = datetime.datetime.strptime(meta_json["date"], "%Y%m%d")
        return (" ".join(references) + " " + meta_json["title"] + " " + date.strftime("%Y")).lower()


def process_files(file_paths: list[str]):
    index = {}

    for file_path in file_paths:
        file_id = get_file_id(file_path)
        content = get_content_to_index(file_path)
        stemmer = SnowballStemmer("russian")
        words = word_tokenize(content)

        def clean_word(word: str):
            return ''.join(e for e in word if e.isalnum())

        stemmed_words = {stemmer.stem(clean_word(word)) for word in words}
        stemmed_words = [word for word in stemmed_words if word]

        for stemmed_word in stemmed_words:
            if stemmed_word not in index:
                index[stemmed_word] = []
            if file_id not in index[stemmed_word]:
                index[stemmed_word].append(file_id)

    return index


def save_index(index_id: str, index: list[str]):
    output_file_path = f"{OUTPUT_PATH}/{index_id}.db.index.json"
    with open(output_file_path, 'w') as index_buffer:
        index_buffer.write(
            json.dumps({
                "_id": "index::" + index_id,
                "in_title": index,
            }, ensure_ascii=False)
        )


if __name__ == "__main__":
    result = process_files(get_file_paths_to_process())
    for key, value in result.items():
        save_index(key, value)
