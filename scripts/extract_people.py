import csv
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "WoWCombatLog.txt"
TEMP_LOG_PATH = BASE_DIR / "temp" / "WoWCombatLog.txt"
OUTPUT_PATH = BASE_DIR / "people.csv"


def extract_names(text):
    names = set()

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        match = re.match(r"^\d+/\d+\s+\d+:\d+:\d+\.\d+\s+(.*)$", line)
        if not match:
            continue

        message = match.group(1)
        if message.startswith("COMBATANT_INFO:"):
            payload = message[len("COMBATANT_INFO:") :].strip()
            fields = payload.split("&")
            if len(fields) > 1:
                name = fields[1].strip()
                if name and name.lower() != "nil":
                    names.add(name)
            continue

        if message.startswith("ZONE_INFO:"):
            continue

        if " begins to cast " in message or " casts " in message:
            name = message.split(" ", 1)[0]
            if name and name[0].isalpha() and " " not in name:
                lowered = name.lower()
                if lowered not in {"you", "your", "nil"}:
                    names.add(name)
            continue

        if " 's " in message:
            name = message.split(" 's ", 1)[0].strip()
            if name and " " not in name:
                lowered = name.lower()
                if lowered not in {"you", "your", "nil"}:
                    names.add(name)

    return sorted(names, key=str.lower)


def main():
    log_path = LOG_PATH if LOG_PATH.exists() else TEMP_LOG_PATH
    if not log_path.exists():
        sys.exit(f"{LOG_PATH} or {TEMP_LOG_PATH} not found")

    text = log_path.read_text(encoding="utf-8", errors="replace")
    names = extract_names(text)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name"])
        for name in names:
            writer.writerow([name])

    print(f"Wrote {OUTPUT_PATH} ({len(names)} names)")


if __name__ == "__main__":
    main()
