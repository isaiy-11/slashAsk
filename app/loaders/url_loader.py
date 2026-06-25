import requests
from bs4 import BeautifulSoup


def extract_url_text(url):

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text