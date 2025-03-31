import re


def split_message(text: str) -> list[str]:
    texts = re.split(r'[.\n]', text)
    return [text for text in texts if text]
