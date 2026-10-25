"""Download the original UCI Bike Sharing Dataset used by the project.

Run from the project root:
    python scripts/download_data.py

The script downloads the official UCI archive and extracts day.csv, hour.csv,
and Readme.txt into data/. It does not generate or replace the original data.
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
UCI_URLS = [
    "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip",
]
GOOGLE_DRIVE_ID = "1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ"


def download(url: str) -> bytes:
    response = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    payload = response.content
    if not payload.startswith(b"PK\x03\x04"):
        raise ValueError(f"Respons dari {url} bukan ZIP dataset yang dikenali.")
    return payload


def download_drive() -> bytes:
    session = requests.Session()
    url = "https://drive.google.com/uc"
    response = session.get(url, params={"export": "download", "id": GOOGLE_DRIVE_ID}, timeout=60)
    response.raise_for_status()
    payload = response.content
    if payload.startswith(b"PK\x03\x04"):
        return payload
    # Google Drive may require a confirmation token for large or scanned files.
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break
    if token:
        response = session.get(url, params={"export": "download", "id": GOOGLE_DRIVE_ID, "confirm": token}, timeout=60)
        response.raise_for_status()
        payload = response.content
    if not payload.startswith(b"PK\x03\x04"):
        raise ValueError("Google Drive tidak mengembalikan arsip ZIP; coba sumber UCI atau periksa koneksi.")
    return payload


def extract(payload: bytes) -> list[str]:
    extracted = []
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        by_name = {Path(name).name.lower(): name for name in archive.namelist() if not name.endswith("/")}
        required = {"day.csv", "hour.csv"}
        if not required.issubset(by_name):
            raise ValueError(f"Arsip tidak memiliki file wajib {sorted(required)}.")
        for name in ["day.csv", "hour.csv", "readme.txt"]:
            if name in by_name:
                target = DATA_DIR / ("Readme.txt" if name == "readme.txt" else name)
                target.write_bytes(archive.read(by_name[name]))
                extracted.append(str(target.relative_to(ROOT)))
    return extracted


def main() -> int:
    errors = []
    payload = None
    for url in UCI_URLS:
        try:
            print(f"Mengunduh dataset dari UCI: {url}")
            payload = download(url)
            break
        except Exception as exc:  # try the next official mirror if necessary
            errors.append(f"{url}: {exc}")
    if payload is None:
        try:
            print("Mencoba tautan Google Drive yang disediakan pada instruksi proyek...")
            payload = download_drive()
        except Exception as exc:
            errors.append(f"Google Drive: {exc}")
    if payload is None:
        print("Gagal mengunduh dataset. Pastikan koneksi internet aktif. Detail:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    try:
        extracted = extract(payload)
    except Exception as exc:
        print(f"Gagal mengekstrak arsip: {exc}", file=sys.stderr)
        return 1
    print("Dataset berhasil disimpan:")
    for path in extracted:
        print(f"- {path}")
    print("Gunakan data/day.csv untuk analisis harian dan dashboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
