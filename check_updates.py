"""Simple Windows 11 update checker (first version of the template).

Sends an HTTP request to the Microsoft Update Catalog and reports whether
the search results page lists any updates. There is no official public API
for this, so the check is intentionally simple and HTML-based.
"""
import sys

import requests

CATALOG_URL = "https://www.catalog.update.microsoft.com/Search.aspx"
NO_RESULTS_MARKER = "No results were found"


def check_windows11_updates(query: str = "Windows 11", timeout: int = 15) -> bool:
    """Return True if the catalog lists updates for the query."""
    resp = requests.get(CATALOG_URL, params={"q": query}, timeout=timeout)
    resp.raise_for_status()
    return NO_RESULTS_MARKER not in resp.text


def main() -> int:
    try:
        found = check_updates_wrapper()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1
    print("Updates found" if found else "No updates found")
    return 0


def check_updates_wrapper() -> bool:
    return check_windows11_updates()


if __name__ == "__main__":
    sys.exit(main())
