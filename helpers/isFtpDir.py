def isFtpDir(target, curDirList):
  targetName = target.split("/")[-1]
  for el in curDirList:
    if el["name"] == targetName and el["directory"] == "d":
      return True
  return False
  pass