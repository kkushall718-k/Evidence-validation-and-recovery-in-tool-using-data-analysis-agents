"""Retrieve the public source archive and verify the exact study CSV; no credentials."""

from pathlib import Path
import hashlib
import io
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.kaggle.com/api/v1/datasets/download/gregorut/videogamesales"
EXPECTED = "e2076095ffcae2a92dbc6de6ecbd54455ee034bb38da550b2dc385e9265d4ebe"
TARGET = ROOT / "data/vgsales.csv"
if TARGET.exists():
    if hashlib.sha256(TARGET.read_bytes()).hexdigest() != EXPECTED:
        raise SystemExit(
            "Existing CSV differs from the study. Preserve it separately before retrieval."
        )
    print("Verified existing study CSV; no download needed.")
else:
    with urllib.request.urlopen(URL, timeout=90) as response:
        archive = zipfile.ZipFile(io.BytesIO(response.read()))
    names = [n for n in archive.namelist() if Path(n).name == "vgsales.csv"]
    if len(names) != 1:
        raise SystemExit(
            "Source archive structure changed; inspect the public source before proceeding."
        )
    csv = archive.read(names[0])
    if hashlib.sha256(csv).hexdigest() != EXPECTED:
        raise SystemExit(
            "Source content changed; do not substitute a new dataset into the recorded study."
        )
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_bytes(csv)
    print("Downloaded and verified the exact study CSV.")
