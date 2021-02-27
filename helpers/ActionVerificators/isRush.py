from constants.actions import Actions as Act

def isRush(i):
  s = i.split(" ")
  if len(s) > 1:
    rushHere = s[0] == Act["Rush"]["h"]
    hAccessorHere = len(s) == 2
    uAccessorHere = len(s) == 4 and s[2] == Act["Rush"]["u"]
    pAccessorHere = len(s) == 6 and s[2] == Act["Rush"]["u"] and s[4] == Act["Rush"]["p"]
    return rushHere and (hAccessorHere or uAccessorHere or pAccessorHere)
  return False
  pass