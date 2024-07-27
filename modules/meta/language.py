import os
from dataclasses import dataclass


@dataclass
class Language:
    name: str
    aliases: list[str]

LANGUAGES: list[Language] = [
    Language(name='ru', aliases=['ru', 'русский']),
]

def extract_language(
    path: str,
) -> str:
    """
    Extract language from the file path.
    """
    folders = os.path.dirname(path).split("/")
    for language in LANGUAGES:
        for alias in language.aliases:
            for folder in folders:
                if folder.lower() == alias.lower():
                    return language.name
    raise Exception(f"Language not found in path {path}")
