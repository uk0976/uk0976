import os
import json
import re
from datetime import datetime, timedelta, timezone
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USERNAME = os.getenv("GITHUB_USERNAME", "uk0976")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    response = requests.get(URL, headers=headers, timeout=15, verify=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate all contribution cells (either td or rect tags with data-date)
    cells = soup.find_all(lambda tag: tag.has_attr("data-date"))
    
    contributions = []
    total_count = 0
    
    # Tooltips or aria-labels often carry exact count, e.g. "5 contributions on July 15, 2026"
    # Or level 0, 1, 2, 3, 4
    for cell in cells:
        date_str = cell.get("data-date")
        level_str = cell.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0
            
        # Try to find count from data-count, inner text, or tooltip
        count = None
        if cell.has_attr("data-count"):
            try:
                count = int(cell["data-count"])
            except ValueError:
                pass
        
        if count is None:
            # Fallback to level estimation if count not explicitly found
            count_map = {0: 0, 1: 1, 2: 3, 3: 6, 4: 10}
            count = count_map.get(level, level)

        # Look for associated tooltips if available
        cell_id = cell.get("id")
        if cell_id:
            tooltip = soup.find("tool-tip", attrs={"for": cell_id})
            if tooltip:
                text = tooltip.get_text()
                match = re.search(r"(\d+)\s+contribution", text)
                if match:
                    count = int(match.group(1))
                elif "No contribution" in text or "0 contribution" in text:
                    count = 0

        contributions.append({
            "date": date_str,
            "level": level,
            "count": count
        })
        total_count += count

    # Sort by date ascending
    contributions.sort(key=lambda x: x["date"])

    # Compute streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = 0

    for day in contributions:
        c = day["count"]
        if c > best_day:
            best_day = c

        if c > 0 or day["level"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Calculate current streak up to today or yesterday
    for day in reversed(contributions):
        if day["count"] > 0 or day["level"] > 0:
            current_streak += 1
        else:
            # Allow today to be 0 without breaking yesterday's streak
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            if day["date"] == today_str and current_streak == 0:
                continue
            break

    data = {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat() + "Z",
        "total_contributions": total_count,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": contributions
    }


    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully fetched {len(contributions)} days ({total_count} total contributions) for {USERNAME}.")

if __name__ == "__main__":
    fetch_contributions()
