from constants.actions import Actions as Act
from utils.trimSpaces import trimSpaces
from constants.environments import environments as envs

class ActionVerifier:
  def __init__(self):
    pass

  def __splitAction(self, action):
    return action.split(" ")
    pass
    
  def isCd(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Cd"]
    return False
    pass

  def isClear(self, action):
    return action == Act["Clear"]
    pass

  def isDelete(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Delete"]
    return False
    pass

  def isDrop(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Drop"]
    return False
    pass

  def isExit(self, action):
    return action == Act["Exit"] or action == Act["ExitShort"]
    pass

  def isHelp(self, action):
    return action == Act["Help"] or action == Act["HelpShort"]
    pass

  def isJump(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      act = splited[0] == Act["Jump"]
      local = splited[1] == envs["Local"]
      remote = splited[1] == envs["Remote"]
      return act and (local or remote)
    return False
    pass

  def isLs(self, action):
    return action == Act["Ls"]
    pass
  
  def isMkdir(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Mkdir"]
    return False
    pass

  def isRush(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      return splited[0] == Act["Rush"]
    return False
    pass

  def isStatus(self, action):
    return action == Act["Status"]
    pass

  def isTake(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Take"]
    return False
    pass

  def isWhereAmI(self, action):
    isAct = action == Act["WhereAmI"]
    isActShort = action == Act["WhereAmIShort"]
    return isAct or isActShort
    pass

  def isWhoAmI(self, action):
    return action == Act["WhoAmI"]
    pass