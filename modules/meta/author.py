from dataclasses import dataclass

@dataclass
class Author:
    code: str
    aliases: list[str]
    canonical_names: dict[str, str]

AUTHORS: list[Author] = [
    Author(
        code='acbsp',
        aliases=['Шрила Прабхупада'],
        canonical_names = {
            'en': 'A. C. Bhaktivedanta Swami Prabhupada',
            'ru': 'А. Ч. Бхактиведанта Свами Прабхупада',
        }
    ),
]

def extract_author(
    path: str
) -> str:
    """
    Extract author from path based on the author names and returns
    it's canonical name. Otherwise raises an exception.
    """
    for author in AUTHORS:
        for alias in author.aliases:
            if alias in path:
                return (author.code, alias)
    raise Exception(f"Author not found in path {path}")
