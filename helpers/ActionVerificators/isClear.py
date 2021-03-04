from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isClear(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["Clear"]
  pass