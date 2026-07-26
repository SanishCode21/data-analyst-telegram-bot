from .url_detector import extract_urls
from .dataset_tool import download_file
from .csv_tool import load_csv

def prepare_dataset_context(user_text):
    urls = extract_urls(user_text)

    if not urls:
        return None

    path = download_file(urls[0])
    df = load_csv(path)

    return f"""
Rows: {len(df)}
Columns: {list(df.columns)}

Sample:
{df.head().to_markdown(index=False)}
"""
