from dataclasses import dataclass

@dataclass
class Source:
    name: str
    aliases: list[str]

SOURCES: list[Source] = [
    Source(name='BG', aliases=['БГ', 'Бхагавад-гита', 'Бхагавад гита']),
]

def extract_source(
    path: str
) -> str:
    """
    Extract source from path based on the source names and returns
    it's canonical name. Otherwise raises an exception.
    """
    for source in SOURCES:
        if any(alias in path for alias in source.aliases):
            return source.name
    raise Exception(f"Source not found in path {path}")
