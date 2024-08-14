import json

from nltk import SnowballStemmer, word_tokenize

INPUT_PATH = "../../../../content/library/"


def get_file_title(file_path: str):
    with open(file_path, 'r') as meta_buffer:
        meta_json = json.load(meta_buffer)
        references = meta_json["references"]
        references = [ref[0] + " " + ".".join(map(str, ref[1:])) for ref in references]
        return " ".join(references) + " " + meta_json["title"]


def open_search_index(filename):
    with open(filename) as f:
        return json.load(f)


def process_query(
    query: str,
    search_index: dir,
):
    stemmer = SnowballStemmer("russian")
    words = word_tokenize(query)

    stemmed_words = {stemmer.stem(word) for word in words}
    stemmed_words = [word for word in stemmed_words if len(word) > 0]

    common_ids = set(search_index.get(stemmed_words[0], []))
    for stemmed_word in stemmed_words[1:]:
        common_ids.intersection_update(search_index.get(stemmed_word, []))

    return common_ids


if __name__ == '__main__':
    user_query = input('Enter a search query: ')
    search_index = open_search_index("search-index.json")
    ids = process_query(user_query, search_index)
    for file_id in ids:
        print(file_id, get_file_title(f"{INPUT_PATH}/{file_id}.meta.json"))
