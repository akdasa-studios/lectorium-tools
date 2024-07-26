import os
from sys import argv
from typing import Callable

from cuid2 import cuid_wrapper

PATH_INPUT = argv[1] if len(argv) > 1 else "input"
CUID_GENERATOR: Callable[[], str] = cuid_wrapper()


def rename_files_with_id(
    folder_path: str
):
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            unique_id = CUID_GENERATOR()
            new_filename = f"{unique_id} {filename}"
            os.rename(
                os.path.join(folder_path, filename),
                os.path.join(folder_path, new_filename)
            )

rename_files_with_id(PATH_INPUT)