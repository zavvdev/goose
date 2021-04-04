import os

def isFtpFileExists(ftp, target, currentPathRemote):
  curDirList = ftp.list(currentPathRemote, extra=True)
  for el in curDirList:
    if el["name"] == target:
      return True
  return False
  pass