from re import search
from modules.meta.source import extract_source


REFERENCE_PATTERNS = [
    r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})\-(?P<part3>\d{2})\.(?P<part4>\d{2})",
    r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})\.(?P<part3>\d{2})-(?P<part4>\d{2})",
    r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})\.(?P<part3>\d{2})",
    r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2}-\d{2})",
    r"(?P<name>\w+)\s(?P<part1>\d{2})\.(?P<part2>\d{2})",
    r"(\w{24})\s(?P<name>\w+)\s(?P<part1>\w+)"
]


def extract_references(
    input: str,
) -> list[str]:
    """
    Extract references from input based on the input string. Returns
    a list of references. Otherwise raises an exception.
    """
    for pattern in REFERENCE_PATTERNS:
        try:
            match = search(pattern, input)
            if match:
                source = extract_source(match.group("name"))
                reference_text = match.group(0)

                if "part3" in match.groupdict():
                    return ([[
                        source,
                        int(match.group("part1")) if match.group("part1").isnumeric() else match.group("part1"),
                        int(match.group("part2")) if match.group("part2").isnumeric() else match.group("part2"),
                        int(match.group("part3")) if match.group("part3").isnumeric() else match.group("part3"),
                    ]], reference_text)
                elif "part2" in match.groupdict():
                    return ([[
                        source,
                        int(match.group("part1")) if match.group("part1").isnumeric() else match.group("part1"),
                        int(match.group("part2")) if match.group("part2").isnumeric() else match.group("part2"),
                    ]], reference_text)
                else:
                    return ([[
                        source,
                        int(match.group("part1")) if match.group("part1").isnumeric() else match.group("part1"),
                    ]], reference_text)
        except Exception as e:
            pass

    source = extract_source(input)
    if source:
        return ([[source]], source)

    raise Exception(f"References not found in input {input}")
