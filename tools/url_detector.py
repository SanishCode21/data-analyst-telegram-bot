import re

URL_PATTERN = r"https?://[^\s]+"

def extract_urls(text: str):
    return re.findall(URL_PATTERN, text)

