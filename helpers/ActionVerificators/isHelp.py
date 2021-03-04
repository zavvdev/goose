from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isHelp(action):
  trimmed = trimSpaces(action)
  return trimmed == Act["Help"] or trimmed == Act["HelpShort"]
  pass