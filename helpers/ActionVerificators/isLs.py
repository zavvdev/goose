from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isLs(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["Ls"]
  pass