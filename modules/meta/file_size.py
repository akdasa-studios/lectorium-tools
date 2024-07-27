import os

def extract_file_size(
    path: str,
) -> int:
    """
    Extract file size from the file path.
    """
    return os.path.getsize(path)
