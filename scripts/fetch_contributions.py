import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "jayanithyan"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def fetch_page():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    return response.text


def parse_contributions(html):
    soup = BeautifulSoup(html, "html.parser")

    days = []

    for element in soup.select("td.ContributionCalendar-day"):
        date = element.get("data-date")
        level = element.get("data-level")

        if not date:
            continue

        try:
            count = 0

            for attr in [
                "data-count",
                "data-contribution-count"
            ]:
                if element.get(attr):
                    count = int(element.get(attr))
                    break

            if count == 0:
                label = element.get("aria-label", "")

                match = re.search(
                    r"(\d+)\s+contribution",
                    label
                )

                if match:
                    count = int(match.group(1))

            days.append({
                "date": date,
                "count": count,
                "level": int(level or 0)
            })

        except (ValueError, TypeError):
            continue

    return days


def main():
    print(f"Fetching contributions for {USERNAME}...")

    html = fetch_page()

    print("Parsing contribution calendar...")

    days = parse_contributions(html)

    if not days:
        raise RuntimeError(
            "No contribution data found."
        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "username": USERNAME,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "days": days
    }

    OUTPUT.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    print(
        f"Saved {len(days)} days to {OUTPUT}"
    )


if __name__ == "__main__":
    main()