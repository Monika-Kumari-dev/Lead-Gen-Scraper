"""
Debug helper: fetch a directory page's raw HTML and save it locally so we
can inspect real class names / structure, instead of guessing selectors blind.

Run with: python inspect_page.py <url>
"""

import sys
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect_page.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Saved {len(response.text)} characters to page_dump.html")
    print("Open it in your browser to inspect.")


if __name__ == "__main__":
    main()