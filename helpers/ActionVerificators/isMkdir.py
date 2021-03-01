from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isMkdir(i):
  trimmed = trimSpaces(i)
  s = trimmed.split(" ")
  if len(s) >= 2:
    return s[0] == Act["Mkdir"]
  return False
  pass