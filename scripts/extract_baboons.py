import re
from pathlib import Path
import sys

SOURCE_PATH = Path("RaidnRank.lua")
OUTPUT_PATH = Path("baboons.csv")

text = SOURCE_PATH.read_text(encoding="utf-8")
match = re.search(r'\["csv"\]\s*=\s*"((?:\\.|[^\"])*)"', text, re.DOTALL)
if not match:
    sys.exit("csv field not found in RaidnRank.lua")

csv_escaped = match.group(1)
# Lua escapes use backslashes; unicode_escape handles \n, \t, \", and \\.
csv_data = bytes(csv_escaped, "utf-8").decode("unicode_escape")

OUTPUT_PATH.write_text(csv_data, encoding="utf-8")
print(f"Wrote {OUTPUT_PATH} ({len(csv_data.splitlines())} lines)")
