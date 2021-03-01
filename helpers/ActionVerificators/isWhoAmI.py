from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isWhoAmI(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["WhoAmI"]
  pass