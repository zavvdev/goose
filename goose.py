import os
import shutil
from pathlib import Path
from ftpretty import ftpretty as FTP
from constants.textStyles import textStyles
from constants.settings import Settings
from helpers.ActionVerificators.isExit import isExit
from helpers.ActionVerificators.isHelp import isHelp
from helpers.ActionVerificators.isRush import isRush
from helpers.ActionVerificators.isLs import isLs
from helpers.ActionVerificators.isJump import isJump
from helpers.ActionVerificators.isClear import isClear
from helpers.ActionVerificators.isWhereAmI import isWhereAmI
from helpers.ActionVerificators.isWhoAmI import isWhoAmI
from helpers.ActionVerificators.isCd import isCd
from helpers.ActionVerificators.isMkdir import isMkdir
from helpers.ActionVerificators.isDelete import isDelete
from helpers.ActionVerificators.isDrop import isDrop
from helpers.ActionVerificators.isTake import isTake
from helpers.ActionVerificators.isStatus import isStatus
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors
from helpers.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from constants.actions import Actions as Act
from helpers.execCmd import execCmd
from helpers.getNextPath import getNextPath
from helpers.getUserConfirm import getUserConfirm
from helpers.getErrorMsg import getErrorMsg
from helpers.getSuccessMsg import getSuccessMsg
from helpers.getInfoMsg import getInfoMsg
from helpers.getSuspendMsg import getSuspendMsg
from helpers.isFtpDir import isFtpDir
from helpers.isFtpFile import isFtpFile
from helpers.getUserInput import getUserInput
from helpers.trimSpaces import trimSpaces
from helpers.getSingleActionParam import getSingleActionParam
from helpers.getTimestamp import getTimestamp
from helpers.isFtpFileExists import isFtpFileExists
from helpers.getInputPrompt import getInputPrompt
from helpers.printServerResponseMsg import printServerResponseMsg
from __locale.printHelp import printHelp

commonNS = getNamespace(nsAccessors["Common"])
rushNS = getNamespace(nsAccessors["Rush"])
jumpNS = getNamespace(nsAccessors["Jump"])
cdNS = getNamespace(nsAccessors["Cd"])
mkdirNS = getNamespace(nsAccessors["Mkdir"])
deleteNS = getNamespace(nsAccessors["Delete"])
dropNS = getNamespace(nsAccessors["Drop"])
takeNS = getNamespace(nsAccessors["Take"])
clearNS = getNamespace(nsAccessors["Clear"])
lsNS = getNamespace(nsAccessors["Ls"])
statusNS = getNamespace(nsAccessors["Status"])


class Goose:
  def __init__(self):
    self.ftp = None
    self.connected = False
    self.loginData = {}
    self.action = ""
    self.env = envs["Local"]
    self.pathLocal = str(Path.home())
    self.pathRemote = ""


  #------------- Utils -------------#


  def pingServer(self, message=True):
    try:
      self.ftp.voidcmd("NOOP")
    except:
      if message:
        print(getErrorMsg(commonNS["connection_lost"]))
      self.setStatusDisconnected()
    pass

  def setStatusDisconnected(self):
    self.ftp = None
    self.connected = False
    self.env = envs["Local"]
    self.pathRemote = ""
    pass


  def login(self):
    d = self.loginData
    try:
      self.ftp = FTP(
        d["host"],
        d["user"],
        d["passwd"],
        port=d["port"],
        timeout=Settings.timeout
      )
      self.ftp.login(user=d["user"], passwd=d["passwd"])
      self.connected = True
      self.env = envs["Remote"]
      self.pathRemote = self.ftp.pwd()
      printServerResponseMsg(self.ftp.getwelcome())
      return True
    except Exception as e:
      self.setStatusDisconnected()
      printServerResponseMsg(e)
      return False
    pass


  def changeLocalPath(self, nextPath):
    os.chdir(nextPath)
    self.pathLocal = nextPath
    pass

  
  def changeRemotePath(self, nextPath):
    self.ftp.cwd(nextPath)
    self.pathRemote = nextPath 
    pass
  

  def rmFtpTree(self, path):
    pathList = self.ftp.list(path, extra=True)
    for target in pathList:
      preparedTargetPath = getNextPath(path, target["name"])
      if target["directory"] == "d":
        self.rmFtpTree(preparedTargetPath)
      else:
        self.ftp.delete(preparedTargetPath)
    self.ftp.rmd(path)
    pass

  
  def deleteLocal(self, target):
    _, targetName = os.path.split(target)
    suspendText = deleteNS["deleting"].format(target=targetName)
    successText = deleteNS["success"]
    localTargetPath = getNextPath(self.pathLocal, target)
    print(getSuspendMsg(commonNS["processing"]))
    if os.path.isfile(localTargetPath):
      confirmMsg = deleteNS["delete_file"].format(fileName=targetName)
      confirmDelFile = getUserConfirm(confirmMsg)
      if confirmDelFile:
        print(getSuspendMsg(suspendText))
        os.remove(localTargetPath)
        print(getSuccessMsg(successText))
    elif os.path.isdir(localTargetPath):
      confirmMsg = deleteNS["delete_dir"].format(dirName=targetName)
      confirmDelDir = getUserConfirm(confirmMsg)
      if confirmDelDir:
        print(getSuspendMsg(suspendText))
        shutil.rmtree(localTargetPath)
        print(getSuccessMsg(successText))
    else:
      raise
    pass


  def deleteRemote(self, target):
    _, targetName = os.path.split(target)
    suspendText = deleteNS["deleting"].format(target=targetName)
    successText = deleteNS["success"]
    remoteTargetPath = getNextPath(self.pathRemote, target)
    print(getSuspendMsg(commonNS["processing"]))
    if isFtpDir(remoteTargetPath, self.ftp):
      confirmMsg = deleteNS["delete_dir"].format(dirName=targetName)
      confirmDelDir = getUserConfirm(confirmMsg)
      if confirmDelDir:
        print(getSuspendMsg(suspendText))
        self.rmFtpTree(remoteTargetPath)
        print(getSuccessMsg(successText))
    elif isFtpFile(remoteTargetPath, self.ftp):
      confirmMsg = deleteNS["delete_file"].format(fileName=targetName)
      confirmDelFile = getUserConfirm(confirmMsg)
      if confirmDelFile:
        print(getSuspendMsg(suspendText))
        self.ftp.delete(remoteTargetPath)
        print(getSuccessMsg(successText))
    else:
      raise
    pass


  def uploadFile(self, targetPath, pathExists, override):
    _, fileName = os.path.split(targetPath)
    fileNameToUpload = fileName
    if not override and pathExists:
      timestamp = getTimestamp()
      fileNameToUpload = "{time}_{file}".format(time=timestamp, file=fileName)
    self.ftp.put(targetPath, fileNameToUpload)
    pass


  def uploadTree(self, targetPath, pathExists, override):
    _, dirName = os.path.split(targetPath)
    dirNameToCreate = dirName
    if not override and pathExists:
      timestamp = getTimestamp()
      dirNameToCreate = "{time}_{dir}".format(time=timestamp, dir=dirName)
    remoteDirPath = getNextPath(self.pathRemote, dirNameToCreate)
    if not pathExists or (pathExists and not override):
      self.ftp.mkd(remoteDirPath)
    self.changeRemotePath(remoteDirPath)
    for el in os.listdir(targetPath):
      elPath = getNextPath(targetPath, el)
      remoteElPath = getNextPath(self.pathRemote, el)
      if os.path.isdir(elPath):
        innerExists = False
        if isFtpFileExists(self.ftp, el, self.pathRemote):
          innerExists = True
        self.uploadTree(elPath, innerExists, True)
      else:
        self.ftp.put(elPath, el)
    backPath = getNextPath(self.pathRemote, "..")
    self.changeRemotePath(backPath)
    pass


  def downloadFile(self, targetPath, pathExists, override):
    _, fileName = os.path.split(targetPath)
    fileNameToCreate = fileName
    if not override and pathExists:
      timestamp = getTimestamp()
      fileNameToCreate = "{time}_{file}".format(time=timestamp, file=fileName)
    localFileName = getNextPath(self.pathLocal, fileNameToCreate)
    self.ftp.get(targetPath, localFileName)
    pass


  def downloadTree(self, targetPath, pathExists, override):
    _, dirName = os.path.split(targetPath)
    dirNameToCreate = dirName
    if not override and pathExists:
      timestamp = getTimestamp()
      dirNameToCreate = "{time}_{dir}".format(time=timestamp, dir=dirName)
    localDirPath = getNextPath(self.pathLocal, dirNameToCreate)
    if not pathExists or (pathExists and not override):
      os.mkdir(localDirPath)
    self.changeLocalPath(localDirPath)
    targetList = self.ftp.list(targetPath, extra=True)
    for el in targetList:
      elPath = getNextPath(targetPath, el["name"])
      localElPath = getNextPath(self.pathLocal, el["name"])
      if el["directory"] == "d":
        innerExists = False
        if os.path.exists(localElPath):
          innerExists = True
        self.downloadTree(elPath, innerExists, True)
      else:
        localFileName = getNextPath(self.pathLocal, el["name"])
        self.ftp.get(elPath, localFileName)  
    backPath = getNextPath(self.pathLocal, "..")
    self.changeLocalPath(backPath)
    pass


  #------------- Actions -------------#


  def cd(self):
    dest = getSingleActionParam(Act["Cd"], self.action)
    if self.env == envs["Local"]:
      nextLocalPath = getNextPath(self.pathLocal, dest)
      if os.path.exists(nextLocalPath):
        self.changeLocalPath(nextLocalPath)  
      else:
        print(getErrorMsg(cdNS["error"].format(dest=nextLocalPath)))
    else:
      self.pingServer()
      if self.connected:
        try:
          nextRemotePath = getNextPath(self.pathRemote, dest)
          self.changeRemotePath(nextRemotePath)
        except:
          print(getErrorMsg(cdNS["error"].format(dest=nextRemotePath)))
    pass


  def clear(self):
    clearResult = execCmd("clear")
    if clearResult:
      print(clearResult)
    else:
      print(getErrorMsg(clearNS["error"]))
    pass


  def delete(self):
    target = getSingleActionParam(Act["Delete"], self.action)
    try:
      if self.env == envs["Local"]:
        self.deleteLocal(target)
      else:
        self.pingServer()
        if self.connected:
          self.deleteRemote(target)
    except:
      print(getErrorMsg(deleteNS["error"].format(target=target)))     
    pass


  def drop(self):
    self.pingServer(message=False)
    if self.connected:
      print(getSuspendMsg(commonNS["processing"]))
      override = False
      pathExists = False
      target = getSingleActionParam(Act["Drop"], self.action)
      targetPath = getNextPath(self.pathLocal, target)
      _, targetName = os.path.split(target)
      if os.path.exists(targetPath):
        if isFtpFileExists(self.ftp, targetName, self.pathRemote):
          pathExists = True
          existsMsg = dropNS["exists"].format(target=targetName)
          confOverrideMsg = getInfoMsg(existsMsg)
          confirmOverride = getUserConfirm(confOverrideMsg)
          if confirmOverride:
            override = True
        try:
          print(getSuspendMsg(dropNS["progress"]))
          if os.path.isfile(targetPath):
            self.uploadFile(targetPath, pathExists, override)
          elif os.path.isdir(targetPath):
            currentRemotePath = self.pathRemote
            self.uploadTree(targetPath, pathExists, override)
            self.changeRemotePath(currentRemotePath)
          else:
            raise Exception("Unable to define local path")
          print(getSuccessMsg(dropNS["success"]))
        except:
          errorMsg = getErrorMsg(dropNS["transfer_error"])
          print(errorMsg)
      else:
        errorMsg = getErrorMsg(dropNS["invalid_path"])
        print(errorMsg)
    else:
      errorMsg = getErrorMsg(dropNS["not_connected"])
      print(errorMsg)
    pass


  def exit(self):
    self.pingServer(message=False)
    if self.connected and self.ftp:
      self.ftp.quit()
    pass


  def help(self):
    printHelp()
    pass


  def jump(self):
    jumpTo = getSingleActionParam(Act["Jump"], self.action)
    if jumpTo == envs["Local"]:
      self.env = envs["Local"]
    else:
      self.pingServer(message=False)
      if self.connected:
        self.env = envs["Remote"]
      else:
        print(getErrorMsg(jumpNS["not_connected"])) 
    pass


  def ls(self):
    if self.env == envs["Remote"]:
      self.pingServer()
      if self.connected:
        try:
          self.ftp.retrlines("LIST")
        except:
          print(getErrorMsg(lsNS["error"]))
    else:
      try:
        if os.path.exists(self.pathLocal):
          os.chdir(self.pathLocal)
          cmd = "ls -l"
          output = execCmd(cmd)
          print(output)
        else:
          raise
      except:
        print(getErrorMsg(lsNS["error"]))
    pass


  def mkdir(self):
    dirName = getSingleActionParam(Act["Mkdir"], self.action)
    try:
      if self.env == envs["Local"]:
        localDirPath = getNextPath(self.pathLocal, dirName)
        os.mkdir(localDirPath)
      else:
        self.pingServer()
        if self.connected:
          remoteDirPath = getNextPath(self.pathRemote, dirName)
          self.ftp.mkd(remoteDirPath)
    except:
      print(getErrorMsg(mkdirNS["error"].format(dirName=dirName)))
    pass


  def rush(self):
    hostStr = getSingleActionParam(Act["Rush"], self.action)
    loginStr = rushNS["login"]["user"]
    passwdStr = rushNS["login"]["passwd"]
    portSrt = rushNS["login"]["port"]
    userInput = getUserInput([loginStr, passwdStr, portSrt])
    self.loginData = {
      "host": hostStr,
      "user": userInput[loginStr],
      "passwd": userInput[passwdStr],
      "port": userInput[portSrt] or Settings.port
    }
    msg = getSuspendMsg(rushNS["connecting"].format(host=self.loginData["host"]))
    print(msg)
    if self.login():
      msg = rushNS["connected"].format(host=self.loginData["host"])
      print(getSuccessMsg(msg))
    else:
      print(getErrorMsg(rushNS["connecting_error"].format(host=self.loginData["host"])))
    pass


  def take(self):
    self.pingServer(message=False)
    if self.connected:
      print(getSuspendMsg(commonNS["processing"]))
      override = False
      pathExists = False
      target = getSingleActionParam(Act["Take"], self.action)
      targetPath = getNextPath(self.pathRemote, target)
      _, targetName = os.path.split(targetPath)
      localTargetPath = getNextPath(self.pathLocal, targetName)
      if os.path.exists(localTargetPath):
        pathExists = True
        existsMsg = takeNS["exists"].format(target=targetName)
        confOverrideMsg = getInfoMsg(existsMsg)
        confirmOverride = getUserConfirm(confOverrideMsg)
        if confirmOverride:
          override = True
      try:
        print(getSuspendMsg(takeNS["progress"]))
        if isFtpDir(targetPath, self.ftp):
          currentLocalPath = self.pathLocal
          self.downloadTree(targetPath, pathExists, override)
          self.changeLocalPath(currentLocalPath)
        else:
          self.downloadFile(targetPath, pathExists, override)
        print(getSuccessMsg(takeNS["success"]))
      except:
        errorMsg = getErrorMsg(takeNS["transfer_error"])
        print(errorMsg)
    else:
      errorMsg = getErrorMsg(takeNS["not_connected"])
      print(errorMsg)
    pass


  def whereAmI(self):
    if self.env == envs["Local"]:
      print(self.pathLocal)
    else:
      self.pingServer()
      if self.connected:
        print(self.pathRemote)
    pass


  def whoAmI(self):
    if self.env == envs["Local"]:
      print(execCmd("whoami"))
    else:
      self.pingServer()
      if self.connected:
        print(self.loginData["user"])
    pass


  def status(self):
    try:
      self.ftp.voidcmd("NOOP")
      printServerResponseMsg(self.ftp.getwelcome())
      print(getSuccessMsg(statusNS["connected_title"]))
      print(statusNS["connected_data"].format(
        host=self.loginData["host"],
        user=self.loginData["user"],
        passwd=self.loginData["passwd"],
        port=self.loginData["port"]
      ))
    except:
      print(getErrorMsg(statusNS["disconnected_title"]))
      self.setStatusDisconnected()
    pass


  #------------- Run -------------#


  def run(self):
    self.clear()
    appNameStyle = textStyles["Bold"] + textStyles["White"]
    print(styledText(appNameStyle + commonNS["app_name"]))
    while True:
      try:
        isRemote = self.env == envs["Remote"]
        env = commonNS["envs"]["remote"] if isRemote else commonNS["envs"]["local"]
        inputText = getInputPrompt(commonNS["input"].format(env=env))
        self.action = input(inputText)
        if isExit(self.action):
          self.exit()
          break
        elif isClear(self.action):
          self.clear()
        elif isHelp(self.action):
          self.help()
        elif isRush(self.action):
          self.rush()
        elif isLs(self.action):
          self.ls()
        elif isJump(self.action):
          self.jump()
        elif isWhereAmI(self.action):
          self.whereAmI()
        elif isWhoAmI(self.action):
          self.whoAmI()
        elif isCd(self.action):
          self.cd()
        elif isMkdir(self.action):
          self.mkdir()
        elif isDelete(self.action):
          self.delete()
        elif isDrop(self.action):
          self.drop()
        elif isTake(self.action):
          self.take()
        elif isStatus(self.action):
          self.status()
        else:
          print(getInfoMsg(commonNS["command_not_found"]))
      except:
        print(getErrorMsg(commonNS["unexpected_error"]))
        break
    pass
