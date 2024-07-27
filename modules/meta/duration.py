from mutagen.mp3 import MP3

def extract_duration(
    path: str,
) -> int:
    """
    Extract file size from the file path.
    """
    audio = MP3(path)
    return int(audio.info.length)
