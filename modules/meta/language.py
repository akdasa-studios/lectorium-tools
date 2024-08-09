import os
from dataclasses import dataclass


@dataclass
class Language:
    name: str
    aliases: list[str]

LANGUAGES: list[Language] = [
    Language(name='ru', aliases=['ru', 'русский']),
    Language(name='en', aliases=['en', 'english']),
]

def extract_language(
    path: str,
) -> list[str]:
    """
    Extract language from the file path.
    """
    result = set()
    folders = os.path.dirname(path).split("/")
    for language in LANGUAGES:
        for alias in language.aliases:
            for folder in folders:
                if alias.lower() in folder.lower():
                    result.add(language.name)

    if not result:
        raise Exception(f"Language not found in path {path}")

    return list(result)