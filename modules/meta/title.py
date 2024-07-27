def extract_title(
    input: str,
    tokens: list[str],
):
    result = input
    for token in tokens:
        result = result.replace(token, "")
    result = (result.strip()
        .replace("  ", " ")
        .replace(".MP3", "")
    )

    if result != "" and not result[0].isalpha():
        raise ValueError(f"Unable to extract title from '{input}' - '{result}' doesn't start with a letter.")

    return result
