from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isStatus(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["Status"]
  pass