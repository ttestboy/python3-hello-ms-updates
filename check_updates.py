"""Windows 11 update checker, version 2.

1. Asks the Microsoft Update Catalog which updates (KB numbers) it lists.
2. Asks the local Windows system which updates (hotfixes) are installed.
3. Correlates the two lists: which catalog updates are installed, which are not.

Deliberately simple: first page of catalog results only, matching by KB number.
"""
import platform
import re
import subprocess
import sys

import requests

CATALOG_URL = "https://www.catalog.update.microsoft.com/Search.aspx"
NO_RESULTS_MARKER = "No results were found"
KB_RE = re.compile(r"KB\d{6,8}", re.IGNORECASE)


def fetch_catalog_kbs(query: str = "Windows 11", timeout: int = 15) -> set:
    """Return the set of KB numbers found on the catalog search page."""
    resp = requests.get(CATALOG_URL, params={"q": query}, timeout=timeout)
    resp.raise_for_status()
    if NO_RESULTS_MARKER in resp.text:
        return set()
    return {kb.upper() for kb in KB_RE.findall(resp.text)}


def get_installed_kbs() -> set:
    """Return KB numbers of updates installed on this machine (Windows only)."""
    if platform.system() != "Windows":
        raise OSError("Installed-update check works only on Windows")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-HotFix | Select-Object -ExpandProperty HotFixID"],
        capture_output=True, text=True, timeout=120, check=True,
    )
    return {line.strip().upper() for line in result.stdout.splitlines() if line.strip()}


def correlate(catalog: set, installed: set):
    """Split catalog KBs into (already installed, not installed)."""
    return sorted(catalog & installed), sorted(catalog - installed)


def main() -> int:
    try:
        catalog = fetch_catalog_kbs()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1
    print(f"Catalog lists {len(catalog)} updates")
    if not catalog:
        return 0

    try:
        installed = get_installed_kbs()
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"Could not read installed updates: {exc}")
        return 1

    present, missing = correlate(catalog, installed)
    print(f"Already installed ({len(present)}): {', '.join(present) or '-'}")
    print(f"Not installed ({len(missing)}): {', '.join(missing) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
