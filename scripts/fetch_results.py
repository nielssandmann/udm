"""Copy U-16 pairings and results from turnering.skak.dk into results.json.

The page reads results.json from the same site, because browsers cannot read
turnering.skak.dk directly. Players are identified by their start number.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

TOURNAMENT_ID = 30508
GROUP_ID = 15432
ROUNDS = 5
URL = "https://turnering.skak.dk/Round/ShowRoundResults/{group}?selectedRound={round}&tournamentId={tour}"
SCORES = {"1": 1, "½": 0.5, "0": 0, "+": 1, "-": 0}


def fetch_round(rnd):
    url = URL.format(group=GROUP_ID, round=rnd, tour=TOURNAMENT_ID)
    req = urllib.request.Request(url, headers={"User-Agent": "udm-what-if/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8")
    body = page.split("<tbody>", 1)[1].split("</tbody>", 1)[0]
    games = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        numbers = re.findall(r'inline-block">\s*(\d*)\.\s*</span>', row)
        result = re.search(r'text-align:center">(.*?)</td>', row, re.S)
        if len(numbers) != 2 or not all(numbers):
            continue  # round not paired yet
        white, black = int(numbers[0]), int(numbers[1])
        text = html.unescape(result.group(1)).strip() if result else ""
        score = None
        if text:
            left = text.split("-")[0].strip() if not text.startswith("-") else "-"
            score = SCORES.get(left)
        games.append({"white": white, "black": black, "score": score, "text": text})
    return games


def main(path):
    rounds = {str(r): fetch_round(r) for r in range(1, ROUNDS + 1)}
    try:
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
    except (OSError, ValueError):
        old = {}
    if old.get("rounds") == rounds:
        print("No changes")
        return
    data = {
        "source": URL.format(group=GROUP_ID, round=1, tour=TOURNAMENT_ID),
        "fetchedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rounds": rounds,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("Updated", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results.json")
