from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isExit(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["Exit"] or trimmed == Act["ExitShort"]
  pass