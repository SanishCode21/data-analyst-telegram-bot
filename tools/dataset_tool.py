import requests
import tempfile

def download_file(url):
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    temp = tempfile.NamedTemporaryFile(delete=False)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    temp.write(response.content)
    temp.close()

    return temp.name

