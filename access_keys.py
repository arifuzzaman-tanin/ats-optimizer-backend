"""Load and validate access keys from the configured public Google Sheet."""

import csv
import io
import urllib.request


SHEET_ID = "1d9I8Vga_I1hSGyGCjcZfhc5q7ypY7uv-jqgzODr39hU"
SHEET_NAME = "key_sheet"

SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/"
    f"tq?tqx=out:csv&sheet={SHEET_NAME}"
)


def get_all_keys():
    """Read all nonempty access keys from the Sheet's first column."""
    with urllib.request.urlopen(SHEET_URL) as response:
        data = response.read().decode("utf-8")

    reader = csv.reader(io.StringIO(data))
    keys = []
    for row in reader:
        if row:
            key = row[0].strip()
            if key:
                keys.append(key)

    return keys


def get_first_key():
    """Return the first access key from the Google Sheet, if one exists."""
    keys = get_all_keys()
    return keys[0] if keys else None


def is_valid_key(provided_key):
    """Check a key against the Google Sheet, ignoring case and outer spaces."""
    keys = get_all_keys()
    provided_key = provided_key.strip().upper()

    for key in keys:
        if key.upper() == provided_key:
            return True

    return False
