from utils.trimSpaces import trimSpaces

def getSingleActionParam(actionName, action):
  trimmed = trimSpaces(action)
  actNameLen = len(actionName)
  result = trimmed[actNameLen:]
  return trimSpaces(result)