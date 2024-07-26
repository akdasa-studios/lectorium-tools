from dataclasses import dataclass, field
from sys import argv
from datetime import date
import os

from db import LOCATIONS, SOURCES
import re
import json


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
    warnings: list[str] = field(default_factory=list)
    original_references: str = ""

def process_directory(directory):
    result: list[FileInfo] = []
    for file_name in os.listdir(directory):
        result.append(process_file_name(file_name))
    return result

def process_file_name(file_name: str) -> FileInfo:
    file_info = FileInfo()

    file_info.file_name  = file_name
    file_info.id         = extract_id(file_name, file_info)
    file_info.location   = extract_location(file_name, file_info)
    file_info.date       = extract_date(file_name, file_info)
    file_info.references = extract_references(file_name, file_info)
    file_info.title      = extract_title(file_name, file_info)

    return file_info

def extract_id(input: str, file_info: FileInfo):
    return input.split(" ")[0]

def extract_title(input: str, file_info: FileInfo):
    result = input

    for location_names in LOCATIONS:
        for location_name in location_names:
            result = result.replace(location_name, "")

    date_patterns = [
        "%d.%m.%Y"
    ]
    for date_pattern in date_patterns:
        result = result.replace(file_info.date.strftime(date_pattern), "")


    result = result.replace(file_info.id, "")
    result = result.replace(file_info.original_references, "")
    result = result.replace(".mp3", "")
    result = result.replace("  ", " ")
    result = result.strip()

    if not result:
        # file_info.warnings.append("No title found")
        result = file_info.location + " " + file_info.date.strftime("%d/%m/%y")

    return result


def extract_location(input: str, file_info: FileInfo):
    for location_names in LOCATIONS:
        canonical_name = location_names[0]
        for location_name in location_names:
            if location_name in input:
                return canonical_name
    file_info.warnings.append("No location found")


def extract_date(input: str, file_info: FileInfo) -> date:
    date_patterns = [
        r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})"
    ]
    for pattern in date_patterns:
        try:
            match = re.search(pattern, input)
            if match:
                day = int(match.group("day"))
                month = int(match.group("month"))
                year = int(match.group("year"))

                if day == 0:
                    day = 1 # TODO: Add warning

                return date(year, month, day)
        except:
            pass
    file_info.warnings.append("No date found")
    return date.min


def extract_references(input: str, file_info: FileInfo) -> list[str]:
    patterns = [
        r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2}-\d{2})",
        r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})"
        # r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2}-\d{2})",
        # r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})"
    ]
    for pattern in patterns:
        try:
            match = re.search(pattern, input)
            if match:
                file_info.original_references = match.group(0)
                source = extract_source(match.group("name"), file_info)
                return [
                    [
                        source,
                        int(match.group("part1")) if match.group("part1").isnumeric() else match.group("part1"),
                        int(match.group("part2")) if match.group("part2").isnumeric() else match.group("part2"),
                    ]
                ]



                # part1 = int(match.group("part1"))
                # part2 = match.group("part2")
                # if "-" in part2:
                #     tokens = list(map(int, part2.split("-")))
                #     return [
                #         [source, int(part1), tokens[0]]
                #     ]
                # else:
                #     return [
                #         [source, int(part1), int(part2)]
                #     ]
        except Exception as e:
            pass

    file_info.warnings.append("No reference found")
    return [[]]

def extract_source(input: str, file_info: FileInfo):
    for source_names in SOURCES:
        canonical_name = source_names[0]
        for source_name in source_names:
            if source_name.lower() == input.lower().strip():
                return canonical_name
    file_info.warnings.append("No source found")

def save_output(file_info: FileInfo):
    file_name = f"{PATH_OUTPUT}/{file_info.id}.meta.json"
    with open(file_name, 'w') as file:
        json.dump(
            {
                "id": file_info.id,
                "title": file_info.title,
                "location": file_info.location,
                "date": file_info.date.strftime("%Y%m%d"),
                "references": file_info.references
            },
            file,
            ensure_ascii=False,
            indent=4)



results = process_directory(PATH_INPUT)
errors_count = 0

for file_info in results:
    if not file_info.warnings:
        save_output(file_info)
        continue

    print(file_info.file_name)
    for warning in file_info.warnings:
        print("  ", warning)
        errors_count += 1


print(f"Errors found {errors_count} in {len(results)} files")