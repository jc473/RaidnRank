# RaidnRank

Workflow for extracting RaidnRank results and preparing the spreadsheet upload.

## Steps
1. In game, run `/rnr extract`.
2. Logout or exit so the file is generated at `WTF/Account/<account>/SavedVariables/RaidnRank.lua`.
3. Copy `RaidnRank.lua` into the same folder as the Python scripts.
4. Run `python extract_baboons.py`.
5. Confirm `raidres.csv` is created (name must be exactly `raidres.csv`) in the same folder.
6. Run `python raidres.py`.
7. Upload `finalized_raidres.csv` to the correct Google Docs spreadsheet and append it.
