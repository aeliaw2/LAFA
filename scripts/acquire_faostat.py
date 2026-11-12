"""Workflow step: download the FAOSTAT Food Security data and check its SHA-256 checksum.

Run from the project folder:  python scripts/acquire_faostat.py

First run:  downloads the file and saves its checksum (commit both files).
Later runs: recomputes the checksum and stops with an error if the file changed.
"""
import hashlib
from pathlib import Path

import requests

# FAOSTAT bulk download for the "Suite of Food Security Indicators" domain.
URL = "https://bulks-faostat.fao.org/production/Food_Security_Data_E_All_Data_(Normalized).zip"

# Project folder = one level up from this script, so paths work from anywhere.
PROJECT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT / "data" / "raw" / "faostat_food_security.zip"
CHECKSUM_FILE = PROJECT / "data" / "raw" / "faostat_food_security.zip.sha256"

# 1. Download the file (skipped if we already have it)
RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
if not RAW_FILE.exists():
    print("Downloading", URL)
    response = requests.get(URL, timeout=300)
    response.raise_for_status()  # stop here if the download failed (e.g., 404)
    with open(RAW_FILE, "wb") as f:
        f.write(response.content)
print(f"File: {RAW_FILE.name} ({RAW_FILE.stat().st_size / 1e6:.1f} MB)")

# 2. Compute the SHA-256 checksum
checksum = hashlib.sha256(RAW_FILE.read_bytes()).hexdigest()
print("SHA-256:", checksum)

# 3. First run: save the checksum. Later runs: compare with the saved one.
if not CHECKSUM_FILE.exists():
    CHECKSUM_FILE.write_text(checksum + "\n")
    print("Saved checksum to", CHECKSUM_FILE.name, "- commit this file.")
elif checksum != CHECKSUM_FILE.read_text().strip():
    raise SystemExit("ERROR: checksum does not match the saved one. "
                     "The file is corrupted or FAO published a new version.")
else:
    print("Checksum OK")
