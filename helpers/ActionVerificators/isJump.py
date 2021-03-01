from constants.actions import Actions as Act
from helpers.trimSpaces import trimSpaces
from constants.environments import environments as envs

def isJump(action):
  trimmed = trimSpaces(action)
  s = trimmed.split(" ")
  if len(s) == 2:
    act = s[0] == Act["Jump"]
    local = s[1] == envs["Local"]
    remote = s[1] == envs["Remote"]
    return act and (local or remote)
  return False
  pass