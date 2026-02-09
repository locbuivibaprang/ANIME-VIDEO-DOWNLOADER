import csv
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# ================= CONFIG =================

CSV_PATH = "CSV_FILES/MOVIES.csv"
COOKIE_DIR = "CSV_FILES"
DOWNLOAD_DIR = r"C:\Users\HP\Videos\PYTHON_VIDS"
MAX_WORKERS = 1   # tune based on bandwidth

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://kwik.cx/",
    "Origin": "https://kwik.cx",
}

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ================= HELPERS =================

def load_cookies(session, cookie_json_path):
    with open(cookie_json_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for c in cookies:
        session.cookies.set(
            name=c["name"],
            value=c["value"],
            domain=c["domain"],
            path=c["path"]
        )

def download_video(row):
    name = row["NAME"].strip()
    post_url = row["POST_URL"].strip()
    token = row["TOKEN"].strip()

    output_path = os.path.join(DOWNLOAD_DIR, name)
    cookie_file = os.path.join(COOKIE_DIR, f"{name}.json")

    with requests.Session() as s:
        s.headers.update(HEADERS)
        load_cookies(s, cookie_file)

        # Resume support
        resume_header = {}
        if os.path.exists(output_path):
            current_size = os.path.getsize(output_path)
            resume_header["Range"] = f"bytes={current_size}-"
        else:
            current_size = 0

        # Retry logic
        for attempt in range(5):
            try:
                r = s.post(
                    post_url,
                    data={"_token": token},
                    headers=resume_header,
                    stream=True,
                    timeout=60,
                    allow_redirects=True
                )
                r.raise_for_status()
                break
            except requests.RequestException:
                print(f"[RETRY {attempt+1}] {name}")
        else:
            print(f"[FAILED] {name}")
            return

        total = int(r.headers.get("Content-Length", 0)) + current_size

        mode = "ab" if current_size else "wb"

        with open(output_path, mode) as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=name[:40],
            initial=current_size,
            leave=False
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

    print(f"[DONE] {name}")


# ================= MAIN =================

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print(f"TOTAL VIDEOS: {len(rows)}")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(download_video, rows)
