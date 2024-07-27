import os

def extract_id(
    path: str,
) -> str:
    """
    Extract file ID from the file path.
    """
    file_name = os.path.basename(path)
    id = file_name.split(" ")[0]
    if len(id) != 24:
        raise Exception(f"ID not found in path {path}")
    return id
