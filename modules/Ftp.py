import os
from ftpretty import ftpretty as FTP
from utils.getNextPath import getNextPath
from utils.getTimestamp import getTimestamp

class Ftp(FTP):
  def exists(self, target, currentPath):
    curDirList = self.list(currentPath, extra=True)
    for el in curDirList:
      if el["name"] == target:
        return True
    return False

  def isDir(self, target):
    path, targetName = os.path.split(target)
    curDirList = self.list(path, extra=True)
    for el in curDirList:
      if el["name"] == targetName and el["directory"] == "d":
        return True
    return False

  def isFile(self, target):
    path, targetName = os.path.split(target)
    curDirList = self.list(path, extra=True)
    for el in curDirList:
      if el["name"] == targetName and el["directory"] != "d":
        return True
    return False

  def rmTree(self, path):
    pathList = self.list(path, extra=True)
    for target in pathList:
      preparedTargetPath = getNextPath(path, target["name"])
      if target["directory"] == "d":
        self.rmTree(preparedTargetPath)
      else:
        self.delete(preparedTargetPath)
    self.rmd(path)

  def putFile(self, targetPath, exists=False, overwrite=True):
    _, fileName = os.path.split(targetPath)
    fileNameToUpload = fileName
    if not overwrite and exists:
      timestamp = getTimestamp()
      fileNameToUpload = "{time}_{file}".format(time=timestamp, file=fileName)
    self.put(targetPath, fileNameToUpload)

  def takeFile(self, targetPath, saveToPath, exists=False, overwrite=True):
    _, fileName = os.path.split(targetPath)
    fileNameToCreate = fileName
    if not overwrite and exists:
      timestamp = getTimestamp()
      fileNameToCreate = "{time}_{file}".format(time=timestamp, file=fileName)
    localFileName = getNextPath(saveToPath, fileNameToCreate)
    self.get(targetPath, localFileName)
