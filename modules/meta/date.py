from re import search
from datetime import date

DATE_PATTERNS = [
    r"(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})",
    r"(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})",
]

def extract_date(
    path: str
) -> date:
    for pattern in DATE_PATTERNS:
        try:
            match = search(pattern, path)
            if match:
                date_text = match.group(0)
                day       = int(match.group("day"))
                month     = int(match.group("month"))
                year      = int(match.group("year"))
                return (date(year, month, day), date_text)
        except:
            pass
    raise Exception(f"Date not found in path {path}")
