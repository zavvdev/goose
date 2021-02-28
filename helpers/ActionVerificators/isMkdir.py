from constants.actions import Actions as Act

def isMkdir(i):
  s = i.split(" ")
  if len(s) == 2:
    return s[0] == Act["Mkdir"]
  return False
  pass