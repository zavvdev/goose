from constants.actions import Actions as Act
from constants.environments import environments as envs

class ActionVerifier:
  def __splitAction(self, action):
    return action.split(" ")
    
  def isCd(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Cd"]
    return False

  def isClear(self, action):
    return action == Act["Clear"]

  def isDelete(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Delete"]
    return False

  def isPut(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Put"]
    return False

  def isExit(self, action):
    return action == Act["Exit"] or action == Act["ExitShort"]

  def isHelp(self, action):
    return action == Act["Help"] or action == Act["HelpShort"]

  def isJump(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      act = splited[0] == Act["Jump"]
      local = splited[1] == envs["Local"]
      remote = splited[1] == envs["Remote"]
      return act and (local or remote)
    return False

  def isLs(self, action):
    return action == Act["Ls"]
  
  def isMkdir(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Mkdir"]
    return False

  def isRush(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      return splited[0] == Act["Rush"]
    return False

  def isStatus(self, action):
    return action == Act["Status"]

  def isTake(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Take"]
    return False

  def isWhereAmI(self, action):
    isAct = action == Act["WhereAmI"]
    isActShort = action == Act["WhereAmIShort"]
    return isAct or isActShort

  def isWhoAmI(self, action):
    return action == Act["WhoAmI"]