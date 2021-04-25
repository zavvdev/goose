from utils.trimSpaces import trimSpaces

# Name: getSingleActionParam
# Desc: Extract single parameter from action
# Args: actionName (string<Key of actions>), action (string)
# Return: string

def getSingleActionParam(actionName, userInput):
  actNameLen = len(actionName)
  result = userInput[actNameLen:]
  return trimSpaces(result)

# ----------------------------------------------------