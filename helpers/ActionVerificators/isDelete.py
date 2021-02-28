from constants.actions import Actions as Act

def isDelete(i):
  s = i.split(" ")
  if len(s) == 2:
    return s[0] == Act["Delete"]
  return False
  pass