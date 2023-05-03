import re


def extract_rib(text: str) -> list[str]:
    """Extracts a RIB from a text.

    Args:
        text (str): The text to extract the RIB from.

    Returns:
        str: The extracted RIB.
    """
    rib_regex = re.compile(r"[A-Z]{2}\d{2}\s?(?:\d{4}\s?){3,}\d*[0-9A-Za-z]?")
    return rib_regex.findall(text)
