import os
import json

from dataclasses import dataclass, field
from sys import argv
from datetime import date

from modules.meta import (
    extract_location, extract_author, extract_id, extract_date,
    extract_references, extract_title, extract_language, extract_file_size,
    extract_duration
)


PATH_INPUT = argv[1] if len(argv) > 1 else "input"
PATH_OUTPUT = argv[2] if len(argv) > 1 else "output"

@dataclass
class FileInfo:
    file_name: str = ""
    id: str = ""
    title: str = ""
    location: str = ""
    date = date.min
    references: list[str] = field(default_factory=list)
    original_references: str = ""
    author: str = ""
    languages: list[str] = field(default_factory=list)
    file_size: int = 0
    duration: int = 0


def process_file(
    file_name: str,
    path: str,
) -> FileInfo:
    print(f"Processing {file_name}")
    file_info = FileInfo()

    file_info.file_name  = file_name
    file_info.id                           = extract_id(os.path.join(path, file_name))
    file_info.location,   token_location   = extract_location(file_name)
    file_info.date,       token_date       = extract_date(os.path.join(path, file_name))
    file_info.references, token_reference  = extract_references(file_name)
    file_info.author,     token_author     = extract_author(path)
    file_info.file_size                    = extract_file_size(os.path.join(path, file_name))
    file_info.duration                     = extract_duration(os.path.join(path, file_name))
    file_info.languages                    = [extract_language(path)]

    file_info.title                        = extract_title(file_name, [
        file_info.id, token_location, token_date, token_reference, ".mp3"
    ]) or f"{token_location} {file_info.date.strftime('%Y-%m-%d')}"

    return file_info


def process_dir(
    path: str,
) -> list[FileInfo]:
    result: list[FileInfo] = []

    for item in os.listdir(path):
        item_full_path = os.path.join(path, item)
        if os.path.isdir(item_full_path):
            file_infos = process_dir(item_full_path)
            result.extend(file_infos)
        else:
            result.append(process_file(item, path))

    return result


def save_output(file_info: FileInfo):
    file_name = f"{PATH_OUTPUT}/{file_info.id}.meta.json"
    with open(file_name, 'w') as file:
        json.dump(
            {
                "id": file_info.id,
                "title": file_info.title,
                "author": file_info.author,
                "location": file_info.location,
                "date": file_info.date.strftime("%Y%m%d"),
                "file_size": file_info.file_size,
                "duration": file_info.duration,
                "references": file_info.references,
                "languages": file_info.languages,
            },
            file,
            ensure_ascii=False,
            indent=2
        )

if __name__ == "__main__":
    results = process_dir(PATH_INPUT)
    for file_info in results:
        save_output(file_info)
