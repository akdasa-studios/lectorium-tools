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
    Source(
        code='sb',
        aliases=['Ш.Б.', 'ШБ'],
        canonical_names={
            'en': { "full": 'Śrīmad-Bhāgavatam', "short": 'SB' },
            'ru': { "full": 'Шримад Бхагаватам', "short": 'ШБ' },
        }),
    Source(
        code='nod',
        aliases=['Nectar_of_Devotion', 'Nectar_of_Devotion'],
        canonical_names={
            'en': { "full": 'Nectar_of_Devotion', "short": 'NoD' },
            'ru': { "full": 'Нектар Преданности', "short": 'НП' },
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
