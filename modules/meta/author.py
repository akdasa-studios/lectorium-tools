from dataclasses import dataclass

@dataclass
class Author:
    name: str
    aliases: list[str]

AUTHORS: list[Author] = [
    Author(name='ACBSP', aliases=['Шрила Прабхупада']),
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
                return (author.name, alias)
    raise Exception(f"Author not found in path {path}")
