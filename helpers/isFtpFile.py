import os

def isFtpFile(target, ftp):
  path, targetName = os.path.split(target)
  curDirList = ftp.list(path, extra=True)
  for el in curDirList:
    if el["name"] == targetName and el["directory"] != "d":
      return True
  return False
  pass