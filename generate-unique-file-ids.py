import os
from sys import argv
from typing import Callable

from cuid2 import cuid_wrapper
import glob

PATH_INPUT = argv[1] if len(argv) > 1 else "input"
CUID_GENERATOR: Callable[[], str] = cuid_wrapper()
PATH_PATTERS = [
    ("Ш.Б.", "ШБ"),
    ("(текст в ID3 теге)", "")
]

def rename_files_with_id(
    file_path: str
):
    file_name = os.path.basename(file_path)
    file_dir  = os.path.dirname(file_path)

    # Fix file name
    fixed_file_name = file_name
    for pattern in PATH_PATTERS:
        fixed_file_name = fixed_file_name.replace(pattern[0], pattern[1])
    if fixed_file_name != file_name:
        print(f"Replacing {file_name} with {fixed_file_name}")
        os.rename(
            file_path,
            os.path.join(file_dir, fixed_file_name)
        )
        file_name = fixed_file_name

    # Check if file name already has a unique id
    if file_name[:24].isalnum() and file_name[24] == ' ':
        return # already has a unique id

    # Add unique id to file name
    unique_id = CUID_GENERATOR()
    file_path_new = f"{unique_id} {file_name}"
    print(f"Adding {unique_id} to {file_name}")
    os.rename(
        file_path,
        os.path.join(file_dir, file_path_new)
    )

file_paths = glob.glob("input/**/*", recursive=True)
for file_path in file_paths:
    if os.path.isfile(file_path):
        rename_files_with_id(file_path)
