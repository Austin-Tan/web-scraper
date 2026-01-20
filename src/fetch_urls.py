import requests
import re
from bs4 import BeautifulSoup


def fetch_html(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ProductCrawler/1.0)"}

    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()  # fails fast on 4xx/5xx
    return response.text


# relies on the BeautifulSoup library to prune extraneous tags (JS, CSS, etc)
# and extract visible text within certain tags.
def remove_noise(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(
        [
            # these tags will never contain useful product information
            "script",
            "style",
            "noscript",
            "iframe",
            "svg",
            "canvas",
            "form",
            # these tags are usually layout / chrome related
            "nav",
            "footer",
            "header",
            "aside",
        ]
    ):
        tag.decompose()

    text_blocks = []
    for tag in soup.find_all(
        [
            "h1",
            "h2",
            "h3",
            "p",
            "li",
            "button",
            "a",
            # TODO: spans can be optional
            "span",
        ]
    ):
        text = tag.get_text(separator=" ", strip=True)
        if text and len(text) > 12:
            text_blocks.append(text)

    cleaned_blocks = []
    for block in text_blocks:
        block = block.lower()
        block = re.sub(r"\s+", " ", block).strip()
        cleaned_blocks.append(block)

    return str.join(", ", cleaned_blocks)


if __name__ == "__main__":
    res = fetch_html("https://funnyfuzzy.com")
    print(remove_noise(res))
