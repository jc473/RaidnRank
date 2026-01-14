import re
import sys
from io import StringIO
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent

RAIDNRANK_PATH = BASE_DIR / "RaidnRank.lua"
RAIDRES_PATH = BASE_DIR / "raidres.csv"
OUTPUT_PATH = BASE_DIR / "finalized_raidres.csv"
COMBAT_LOG_PATH = BASE_DIR / "WoWCombatLog.txt"

try:
    from extract_people import extract_names as extract_log_names
except ImportError:
    extract_log_names = None

# Only these ranks are eligible to be doubled.
eligible_ranks = {"Core Silverback", "Officer Wukong", "Wise Monkey"}
# Only these ranks are included in the finalized output.
included_ranks = eligible_ranks | {"Raider Gorilla"}


def load_guild_csv():
    text = RAIDNRANK_PATH.read_text(encoding="utf-8")
    match = re.search(r'\["csv"\]\s*=\s*"((?:\\.|[^\"])*)"', text, re.DOTALL)
    if not match:
        sys.exit("csv field not found in RaidnRank.lua")

    csv_escaped = match.group(1)
    # Lua escapes use backslashes; unicode_escape handles \n, \t, \", and \\.
    csv_data = bytes(csv_escaped, "utf-8").decode("unicode_escape")
    return pd.read_csv(StringIO(csv_data))


def main():
    df = pd.read_csv(RAIDRES_PATH)
    guild = load_guild_csv()

    if "officernote" not in guild.columns:
        guild["officernote"] = ""

    name_to_rank = guild.set_index("name")["rank"]
    name_to_officernote = guild.set_index("name")["officernote"]

    df["rank"] = df["Attendee"].map(name_to_rank)
    df["officernote"] = df["Attendee"].map(name_to_officernote)

    mask_included = df["rank"].isin(included_ranks)
    mask_eligible = df["rank"].isin(eligible_ranks)
    mask_alt = df["officernote"].str.contains("alt", case=False, na=False)

    # Include only allowed ranks, excluding alts, and duplicate eligible rows.
    df_included = df[mask_included & ~mask_alt]

    if COMBAT_LOG_PATH.exists() and extract_log_names is not None:
        log_text = COMBAT_LOG_PATH.read_text(encoding="utf-8", errors="replace")
        log_names = set(extract_log_names(log_text))
        if log_names:
            print("Names found in WoWCombatLog.txt:")
            for name in sorted(log_names, key=str.lower):
                print(name)
        df_included = df_included[df_included["Attendee"].isin(log_names)]
    df_doubled = pd.concat(
        [df_included, df_included[mask_eligible]],
        ignore_index=True,
    )
    df_doubled = df_doubled.drop(columns=["rank", "officernote"])

    df_doubled.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved as {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
