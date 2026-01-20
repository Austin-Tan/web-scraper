import csv
from pathlib import Path

from load_config import load_config
from fetch_urls import fetch_html, remove_noise, tokenize_text
from analyze import prune_tokens

DATA_DIR = Path("data")
INPUT_URLS_PATH = DATA_DIR / "input_urls.txt"
OUTPUT_CSV_PATH = DATA_DIR / "output.csv"


def load_urls() -> list[str]:
    if not INPUT_URLS_PATH.exists():
        raise FileNotFoundError(f"{INPUT_URLS_PATH} not found")

    with INPUT_URLS_PATH.open() as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def run():
    config = load_config()
    threshold = config["keyword_threshold"]
    max_keywords = config["max_keywords"]

    urls = load_urls()

    url_to_tokens = {}
    for url in urls:
        try:
            html = fetch_html(url)
            text = remove_noise(html)
            tokens = tokenize_text(text)

            url_to_tokens[url] = tokens
        except Exception as e:
            print(f"error scraping url {url}: {e}")

    print(f"attempting to prune tokens for {len(url_to_tokens)} urls")
    urls_to_keywords = prune_tokens(
        url_to_tokens, threshold=threshold, max_keywords=max_keywords
    )

    rows = []
    for url, data in urls_to_keywords.items():
        rows.append(
            {
                "url": url,
                "product_type": data["product_type"],
                "keywords": " ".join(data["keywords"]),
            }
        )

    print(f"attempting to prune tokens for {len(url_to_tokens)} urls")

    write_csv(rows)


def write_csv(rows: list[dict]):
    """
    Writes CSV with 'url', 'product_type', 'keywords'.
    Keywords are stored as a **space-separated string** in a single column.
    """
    if not rows:
        return

    fieldnames = rows[0].keys()

    with OUTPUT_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    run()
