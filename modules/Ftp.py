import os
from ftpretty import ftpretty as FTP
from utils.getNextPath import getNextPath
from utils.getTimestamp import getTimestamp
from modules.Namespace import Namespace
from modules.Message import Message

ns = Namespace()
msg = Message()

# Name: Ftp
# Desc: Provide additional features for ftp.
#       Expand capabilities of inherited module
# Inherits: ftpretty
# Methods: 
#   - exists (check if a file exists)
#   - isDir (check if a file is a directory)
#   - isFile (check if a file is a file)
#   - rmTree (delete a file tree)
#   - putFile (upload a single file to the server)
#   - getFile (download a single file from the server)
#   - putTree (upload a file tree to the server)
#   - getTree (download a file tree from the server)

class Ftp(FTP):

  # Name: exists
  # Desc: Check if a file exists
  # Args: target (string), currentPath (string)
  # Return: boolean

  def exists(self, target, currentPath):
    curDirList = self.list(currentPath, extra=True)
    for el in curDirList:
      if el["name"] == target:
        return True
    return False
    
  # ----------------------------------------------------

  # Name: isDir
  # Desc: Check if a file is a directory
  # Args: target (string)
  # Return: boolean

  def isDir(self, target):
    path, targetName = os.path.split(target)
    curDirList = self.list(path, extra=True)
    for el in curDirList:
      if el["name"] == targetName and el["directory"] == "d":
        return True
    return False

  # ----------------------------------------------------

  # Name: isFile
  # Desc: Check if a file is a file
  # Args: target (string)
  # Return: boolean

  def isFile(self, target):
    path, targetName = os.path.split(target)
    curDirList = self.list(path, extra=True)
    for el in curDirList:
      if el["name"] == targetName and el["directory"] != "d":
        return True
    return False

  # ----------------------------------------------------

  # Name: rmTree
  # Desc: Delete a file tree
  # Args: path (string)
  # Return: void

  def rmTree(self, path):
    pathList = self.list(path, extra=True)
    for target in pathList:
      preparedTargetPath = getNextPath(path, target["name"])
      if target["directory"] == "d":
        self.rmTree(preparedTargetPath)
      else:
        msg.default(ns.common["deleting"] + preparedTargetPath)
        self.delete(preparedTargetPath)
    self.rmd(path)

  # ----------------------------------------------------

  # Name: putFile
  # Desc: Upload a single file to the server
  # Args: targetPath (string),
  #       exists (boolean=False),
  #       overwrite (boolean=True)
  # Return: void

  def putFile(self, targetPath, exists=False, overwrite=True):
    _, fileName = os.path.split(targetPath)
    fileNameToUpload = fileName
    if not overwrite and exists:
      timestamp = getTimestamp()
      fileNameToUpload = "{time}_{file}".format(time=timestamp, file=fileName)
    msg.default(ns.common["uploading"] + targetPath)
    self.put(targetPath, fileNameToUpload)

  # ----------------------------------------------------

  # Name: getFile
  # Desc: Download a single file from the server
  # Args: targetPath (string),
  #       exists (boolean=False),
  #       overwrite (boolean=True)
  # Return: void

  def getFile(self, targetPath, saveToPath, exists=False, overwrite=True):
    _, fileName = os.path.split(targetPath)
    fileNameToCreate = fileName
    if not overwrite and exists:
      timestamp = getTimestamp()
      fileNameToCreate = "{time}_{file}".format(time=timestamp, file=fileName)
    localFileName = getNextPath(saveToPath, fileNameToCreate)
    msg.default(ns.common["downloading"] + targetPath)
    self.get(targetPath, localFileName)

  # ----------------------------------------------------

  # Name: putTree
  # Desc: Upload a file tree to the server
  # Args: targetPath (string),
  #       exists (boolean=False),
  #       overwrite (boolean=True)
  # Return: void

  def putTree(self, targetPath, exists=False, overwrite=True):
    _, dirName = os.path.split(targetPath)
    dirNameToCreate = dirName
    if not overwrite and exists:
      timestamp = getTimestamp()
      dirNameToCreate = "{time}_{dir}".format(time=timestamp, dir=dirName)
    remoteDirPath = getNextPath(self.pwd(), dirNameToCreate)
    if not exists or (exists and not overwrite):
      self.mkd(remoteDirPath)
    self.cwd(remoteDirPath)
    for el in os.listdir(targetPath):
      elPath = getNextPath(targetPath, el)
      remoteElPath = getNextPath(self.pwd(), el)
      if os.path.islink(elPath):
        msg.default(ns.common["skipping_symlink"] + elPath)
        continue
      if os.path.isdir(elPath):
        innerExists = False
        if self.exists(el, self.pwd()):
          innerExists = True
        msg.default(ns.common["uploading"] + elPath)
        self.putTree(elPath, innerExists)
      else:
        msg.default(ns.common["uploading"] + elPath)
        self.put(elPath, el)
    backPath = getNextPath(self.pwd(), "..")
    self.cwd(backPath)

  # ----------------------------------------------------

  # Name: getTree
  # Desc: Download a file tree from the server
  # Args: targetPath (string),
  #       exists (boolean=False),
  #       overwrite (boolean=True)
  # Return: void

  def getTree(self, targetPath, exists=False, overwrite=True):
    _, dirName = os.path.split(targetPath)
    dirNameToCreate = dirName
    if not overwrite and exists:
      timestamp = getTimestamp()
      dirNameToCreate = "{time}_{dir}".format(time=timestamp, dir=dirName)
    localDirPath = getNextPath(os.getcwd(), dirNameToCreate)
    if not exists or (exists and not overwrite):
      os.mkdir(localDirPath)
    os.chdir(localDirPath)
    targetList = self.list(targetPath, extra=True)
    for el in targetList:
      elPath = getNextPath(targetPath, el["name"])
      localElPath = getNextPath(os.getcwd(), el["name"])
      if el["directory"] == "d":
        innerExists = False
        if os.path.exists(localElPath):
          innerExists = True
        msg.default(ns.common["downloading"] + elPath)
        self.getTree(elPath, innerExists)
      else:
        localFileName = getNextPath(os.getcwd(), el["name"])
        msg.default(ns.common["downloading"] + elPath)
        self.get(elPath, localFileName)  
    backPath = getNextPath(os.getcwd(), "..")
    os.chdir(backPath)

  # ----------------------------------------------------