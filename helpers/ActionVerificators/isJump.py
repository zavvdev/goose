from constants.actions import Actions as Act

def isJump(i):
  s = i.split(" ")
  if len(s) == 2:
    act = s[0] == Act["Jump"]["act"]
    local = s[1] == Act["Jump"]["local"]
    remote = s[1] == Act["Jump"]["remote"]
    return act and (local or remote)
  return False
  pass