from constants.actions import Actions as Act
from constants.environments import environments as envs

# Name: ActionVerifier
# Desc: Provide the ability to check the entered command
#       for coincidence with application actions
# Inherits: None
# Methods: 
#   - __splitAction (split action by Space symbol)
#   - isCd (check for a match with the Cd action)
#   - isClear (check for a match with the Clear action)
#   - isDelete (check for a match with the Delete action)
#   - isPut (check for a match with the Put action)
#   - isExit (check for a match with the Exit action)
#   - isHelp (check for a match with the Help action)
#   - isJump (check for a match with the Jump action)
#   - isLs (check for a match with the Ls action)
#   - isMkdir (check for a match with the Mkdir action)
#   - isRush (check for a match with the Rush action)
#   - isStatus (check for a match with the Status action)
#   - isTake (check for a match with the Take action)
#   - isWhereAmI (check for a match with the WhereAmI action)
#   - isWhoAmI (check for a match with the WhoAmI action)

class ActionVerifier:

  # Name: __splitAction
  # Desc: Split action by Space symbol
  # Args: action (string)
  # Return: Array of strings

  def __splitAction(self, action):
    return action.split(" ")

  # ----------------------------------------------------

  # Name: isCd
  # Desc: Check for a match with the Cd action
  # Args: action (string)
  # Return: boolean
    
  def isCd(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Cd"]
    return False

  # ----------------------------------------------------

  # Name: isClear
  # Desc: Check for a match with the Clear action
  # Args: action (string)
  # Return: boolean

  def isClear(self, action):
    return action == Act["Clear"]

  # ----------------------------------------------------

  # Name: isDelete
  # Desc: Check for a match with the Delete action
  # Args: action (string)
  # Return: boolean

  def isDelete(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Delete"]
    return False

  # ----------------------------------------------------

  # Name: isPut
  # Desc: Check for a match with the Put action
  # Args: action (string)
  # Return: boolean

  def isPut(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Put"]
    return False

  # ----------------------------------------------------

  # Name: isExit
  # Desc: Check for a match with the Exit action
  # Args: action (string)
  # Return: boolean

  def isExit(self, action):
    return action == Act["Exit"] or action == Act["ExitShort"]

  # ----------------------------------------------------

  # Name: isHelp
  # Desc: Check for a match with the Help action
  # Args: action (string)
  # Return: boolean

  def isHelp(self, action):
    return action == Act["Help"] or action == Act["HelpShort"]

  # ----------------------------------------------------

  # Name: isJump
  # Desc: Check for a match with the Jump action
  # Args: action (string)
  # Return: boolean

  def isJump(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      act = splited[0] == Act["Jump"]
      local = splited[1] == envs["Local"]
      remote = splited[1] == envs["Remote"]
      return act and (local or remote)
    return False

  # ----------------------------------------------------

  # Name: isLs
  # Desc: Check for a match with the Ls action
  # Args: action (string)
  # Return: boolean

  def isLs(self, action):
    return action == Act["Ls"]
  
  # ----------------------------------------------------

  # Name: isMkdir
  # Desc: Check for a match with the Mkdir action
  # Args: action (string)
  # Return: boolean

  def isMkdir(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Mkdir"]
    return False

  # ----------------------------------------------------

  # Name: isRush
  # Desc: Check for a match with the Rush action
  # Args: action (string)
  # Return: boolean

  def isRush(self, action):
    splited = self.__splitAction(action)
    if len(splited) == 2:
      return splited[0] == Act["Rush"]
    return False

  # ----------------------------------------------------

  # Name: isStatus
  # Desc: Check for a match with the Status action
  # Args: action (string)
  # Return: boolean

  def isStatus(self, action):
    return action == Act["Status"]

  # ----------------------------------------------------

  # Name: isTake
  # Desc: Check for a match with the Take action
  # Args: action (string)
  # Return: boolean

  def isTake(self, action):
    splited = self.__splitAction(action)
    if len(splited) >= 2:
      return splited[0] == Act["Take"]
    return False

  # ----------------------------------------------------

  # Name: isWhereAmI
  # Desc: Check for a match with the WhereAmI action
  # Args: action (string)
  # Return: boolean

  def isWhereAmI(self, action):
    isAct = action == Act["WhereAmI"]
    isActShort = action == Act["WhereAmIShort"]
    return isAct or isActShort

  # ----------------------------------------------------

  # Name: isWhoAmI
  # Desc: Check for a match with the WhoAmI action
  # Args: action (string)
  # Return: boolean

  def isWhoAmI(self, action):
    return action == Act["WhoAmI"]

  # ----------------------------------------------------