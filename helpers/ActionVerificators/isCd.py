from constants.actions import Actions as Act

def isCd(i):
  s = i.split(" ")
  if len(s) > 1:
    return s[0] == Act["Cd"]
  return False
  pass