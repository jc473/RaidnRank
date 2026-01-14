local addonName = "RaidnRank"

RaidnRankDB = RaidnRankDB or {}

local pendingExport = false
local exportDelay = 0
local exportElapsed = 0

local function EscapeCSV(value)
  if value == nil then
    return ""
  end

  value = tostring(value)
  if string.find(value, "[\",\n]") then
    value = string.gsub(value, "\"", "\"\"")
    return "\"" .. value .. "\""
  end

  return value
end

local function BuildExport()
  local count = GetNumGuildMembers()
  local entries = {}
  local lines = { "name,rank,officernote" }

  for i = 1, count do
    local name, rank, rankIndex, level, class, zone, note, officernote, online = GetGuildRosterInfo(i)
    if name and rank then
      table.insert(entries, { name = name, rank = rank, officernote = officernote })
      table.insert(lines, EscapeCSV(name) .. "," .. EscapeCSV(rank) .. "," .. EscapeCSV(officernote))
    end
  end

  RaidnRankDB.lastExport = {
    time = date("%Y-%m-%d %H:%M:%S"),
    guild = GetGuildInfo("player"),
    count = count,
    entries = entries,
    csv = table.concat(lines, "\n"),
  }

  DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] Exported " .. count .. " members.")
  DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] CSV stored in SavedVariables/RaidnRank.lua")
end

local function PrintExport()
  if not RaidnRankDB.lastExport then
    DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] No export data yet. Use /rnr export first.")
    return
  end

  local export = RaidnRankDB.lastExport
  DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] Guild: " .. (export.guild or "Unknown") .. " | Members: " .. export.count)
  for _, entry in ipairs(export.entries) do
    DEFAULT_CHAT_FRAME:AddMessage(entry.name .. "\t" .. entry.rank .. "\t" .. (entry.officernote or ""))
  end
end

local function PrintCSV()
  if not RaidnRankDB.lastExport or not RaidnRankDB.lastExport.csv then
    DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] No CSV data yet. Use /rnr export first.")
    return
  end

  for line in string.gfind(RaidnRankDB.lastExport.csv, "[^\n]+") do
    DEFAULT_CHAT_FRAME:AddMessage(line)
  end
end

SLASH_RAIDNRANK1 = "/rnr"
SlashCmdList["RAIDNRANK"] = function(msg)
  msg = msg and string.lower(msg) or ""
  if msg == "export" then
    pendingExport = true
    exportElapsed = 0
    exportDelay = 1.0
    SetGuildRosterShowOffline(true)
    GuildRoster()
    DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] Requesting guild roster...")
  elseif msg == "print" then
    PrintExport()
  elseif msg == "csv" then
    PrintCSV()
  else
    DEFAULT_CHAT_FRAME:AddMessage("[RaidnRank] Commands: /rnr export | /rnr print | /rnr csv")
  end
end

local frame = CreateFrame("Frame")
frame:SetScript("OnUpdate", function()
  if not pendingExport then
    return
  end

  exportElapsed = exportElapsed + arg1
  if exportElapsed >= exportDelay then
    pendingExport = false
    BuildExport()
  end
end)
