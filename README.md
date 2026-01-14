# RaidnRank

Workflow for extracting RaidnRank results and preparing the spreadsheet upload.

## Steps
1. In game, run `/rnr export`.
2. Logout or exit so the file is generated at `WTF/Account/<account>/SavedVariables/RaidnRank.lua`.
3. Copy `RaidnRank.lua` into `scripts/temp`.
4. Confirm `raidres.csv` is created (name must be exactly `raidres.csv`) in `scripts/temp`.
5. Run `python raidres.py` from the `scripts` folder (or double-click `run_raidres.bat`).
6. (Optional) Place `WoWCombatLog.txt` in the `scripts/temp` folder if you want to filter to names seen in the combat log (name must be exactly `WoWCombatLog.txt`).
6. Upload `finalized_raidres.csv` to the correct Google Docs spreadsheet and append it.

Notes:
- Officer notes are exported into the CSV; if a member's officer note contains `alt` (case-insensitive), they will not be duplicated.
- Eligible ranks are still doubled automatically; no `x2` is needed in the SR sheet.
-extract_baboons.py is just a helper
