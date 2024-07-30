from dataclasses import dataclass

@dataclass
class Source:
    code: str
    aliases: list[str]
    canonical_names: dict[str, dict[str, str]]

SOURCES: list[Source] = [
    Source(
        code='bg',
        aliases=['БГ', 'Бхагавад-гита', 'Бхагавад гита'],
        canonical_names={
            'en': { "full": 'Bhagavad Gita', "short": 'BG' },
            'ru': { "full": 'Бхагавад-гита', "short": 'БГ' },
        }),
]

def extract_source(
    path: str
) -> str:
    """
    Extract source from path based on the source names and returns
    it's canonical code. Otherwise raises an exception.
    """
    for source in SOURCES:
        if any(alias in path for alias in source.aliases):
            return source.code
    raise Exception(f"Source not found in path {path}")
