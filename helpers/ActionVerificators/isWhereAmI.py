from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces

def isWhereAmI(action):
  trimmed = trimSpaces(action)
  isAct = trimmed == Act["WhereAmI"]
  isActShort = trimmed == Act["WhereAmIShort"]
  return isAct or isActShort
  pass