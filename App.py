import os
import shutil
from pathlib import Path

from modules.ActionVerifier import ActionVerifier
from modules.Message import Message
from modules.Ftp import Ftp
from modules.Interact import Interact
from modules.Namespace import Namespace

from constants.settings import settings
from constants.environments import environments as envs
from constants.actions import Actions as Act

from utils.execCmd import execCmd
from utils.getNextPath import getNextPath
from utils.trimSpaces import trimSpaces
from utils.getSingleActionParam import getSingleActionParam
from utils.getTimestamp import getTimestamp
from utils.getInputPrompt import getInputPrompt

Av = ActionVerifier()
Msg = Message()
Interact = Interact()
Ns = Namespace()

class App:
  def __init__(self):
    self.ftp = None
    self.connected = False
    self.loginData = {}
    self.action = ""
    self.env = envs["Local"]
    self.pathLocal = str(Path.home())
    self.pathRemote = ""


  #------------- Utils -------------#


  def processAction(self, action):
    return trimSpaces(action)

  def pingServer(self, message=True):
    try:
      self.ftp.voidcmd("NOOP")
    except:
      if message:
        Msg.error(Ns.common["connection_lost"])
      self.setStatusDisconnected()


  def setStatusDisconnected(self):
    self.ftp = None
    self.connected = False
    self.env = envs["Local"]
    self.pathRemote = ""


  def login(self):
    loginData = self.loginData
    try:
      self.ftp = Ftp(
        loginData["host"],
        loginData["user"],
        loginData["passwd"],
        port=loginData["port"],
        timeout=settings["timeout"]
      )
      self.ftp.login(user=loginData["user"], passwd=loginData["passwd"])
      self.connected = True
      self.env = envs["Remote"]
      self.pathRemote = self.ftp.pwd()
      Msg.serverResponse(self.ftp.getwelcome())
      return True
    except Exception as e:
      self.setStatusDisconnected()
      Msg.serverResponse(e)
      return False


  def changeLocalPath(self, nextPath):
    os.chdir(nextPath)
    self.pathLocal = nextPath

  
  def changeRemotePath(self, nextPath):
    self.ftp.cwd(nextPath)
    self.pathRemote = nextPath 
  

  def rmFtpTree(self, path):
    pathList = self.ftp.list(path, extra=True)
    for target in pathList:
      preparedTargetPath = getNextPath(path, target["name"])
      if target["directory"] == "d":
        self.rmFtpTree(preparedTargetPath)
      else:
        self.ftp.delete(preparedTargetPath)
    self.ftp.rmd(path)

  
  def deleteLocal(self, target):
    _, targetName = os.path.split(target)
    suspendText = Ns.delete["deleting"].format(target=targetName)
    successText = Ns.delete["success"]
    localTargetPath = getNextPath(self.pathLocal, target)
    Msg.suspend(Ns.common["processing"])
    if os.path.isfile(localTargetPath):
      confirmMsg = Ns.delete["delete_file"].format(fileName=targetName)
      confirmDelFile = Interact.confirm(confirmMsg)
      if confirmDelFile:
        Msg.suspend(suspendText)
        os.remove(localTargetPath)
        Msg.success(successText)
    elif os.path.isdir(localTargetPath):
      confirmMsg = Ns.delete["delete_dir"].format(dirName=targetName)
      confirmDelDir = Interact.confirm(confirmMsg)
      if confirmDelDir:
        Msg.suspend(suspendText)
        shutil.rmtree(localTargetPath)
        Msg.success(successText)
    else:
      raise


  def deleteRemote(self, target):
    _, targetName = os.path.split(target)
    suspendText = Ns.delete["deleting"].format(target=targetName)
    successText = Ns.delete["success"]
    remoteTargetPath = getNextPath(self.pathRemote, target)
    if self.ftp.isDir(remoteTargetPath):
      confirmMsg = Ns.delete["delete_dir"].format(dirName=targetName)
      confirmDelDir = Interact.confirm(confirmMsg)
      if confirmDelDir:
        Msg.suspend(suspendText)
        self.rmFtpTree(remoteTargetPath)
        Msg.success(successText)
    elif self.ftp.isFile(remoteTargetPath):
      confirmMsg = Ns.delete["delete_file"].format(fileName=targetName)
      confirmDelFile = Interact.confirm(confirmMsg)
      if confirmDelFile:
        Msg.suspend(suspendText)
        self.ftp.delete(remoteTargetPath)
        Msg.success(successText)
    else:
      raise


  def uploadFile(self, targetPath, pathExists, override):
    _, fileName = os.path.split(targetPath)
    fileNameToUpload = fileName
    if not override and pathExists:
      timestamp = getTimestamp()
      fileNameToUpload = "{time}_{file}".format(time=timestamp, file=fileName)
    self.ftp.put(targetPath, fileNameToUpload)


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
        if self.ftp.exists(el, self.pathRemote):
          innerExists = True
        self.uploadTree(elPath, innerExists, True)
      else:
        self.ftp.put(elPath, el)
    backPath = getNextPath(self.pathRemote, "..")
    self.changeRemotePath(backPath)


  def downloadFile(self, targetPath, pathExists, override):
    _, fileName = os.path.split(targetPath)
    fileNameToCreate = fileName
    if not override and pathExists:
      timestamp = getTimestamp()
      fileNameToCreate = "{time}_{file}".format(time=timestamp, file=fileName)
    localFileName = getNextPath(self.pathLocal, fileNameToCreate)
    self.ftp.get(targetPath, localFileName)


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


  #------------- Actions -------------#


  def cd(self):
    dest = getSingleActionParam(Act["Cd"], self.action)
    if self.env == envs["Local"]:
      nextLocalPath = getNextPath(self.pathLocal, dest)
      if os.path.exists(nextLocalPath):
        self.changeLocalPath(nextLocalPath)  
      else:
        Msg.error(Ns.cd["error"].format(dest=nextLocalPath))
    else:
      self.pingServer()
      if self.connected:
        try:
          nextRemotePath = getNextPath(self.pathRemote, dest)
          self.changeRemotePath(nextRemotePath)
        except:
          Msg.error(Ns.cd["error"].format(dest=nextRemotePath))


  def clear(self):
    clearResult = execCmd("clear")
    if clearResult:
      print(clearResult)
    else:
      Msg.error(Ns.clear["error"])


  def delete(self):
    target = getSingleActionParam(Act["Delete"], self.action)
    Msg.suspend(Ns.common["processing"])
    try:
      if self.env == envs["Local"]:
        self.deleteLocal(target)
      else:
        self.pingServer()
        if self.connected:
          self.deleteRemote(target)
    except:
      Msg.error(Ns.delete["error"].format(target=target))   


  def put(self):
    self.pingServer(message=False)
    if self.connected:
      Msg.suspend(Ns.common["processing"])
      override = False
      pathExists = False
      target = getSingleActionParam(Act["Put"], self.action)
      targetPath = getNextPath(self.pathLocal, target)
      _, targetName = os.path.split(target)
      if os.path.exists(targetPath):
        if self.ftp.exists(targetName, self.pathRemote):
          pathExists = True
          existsMsg = Ns.put["exists"].format(target=targetName)
          confirmOverride = Interact.confirm(existsMsg)
          if confirmOverride:
            override = True
        try:
          Msg.suspend(Ns.put["progress"])
          if os.path.isfile(targetPath):
            self.uploadFile(targetPath, pathExists, override)
          elif os.path.isdir(targetPath):
            currentRemotePath = self.pathRemote
            self.uploadTree(targetPath, pathExists, override)
            self.changeRemotePath(currentRemotePath)
          else:
            raise Exception("Unable to define local path")
          Msg.success(Ns.put["success"])
        except:
          Msg.error(Ns.put["transfer_error"])
      else:
        Msg.error(Ns.put["invalid_path"])
    else:
      Msg.error(Ns.put["not_connected"])


  def exit(self):
    self.pingServer(message=False)
    if self.connected and self.ftp:
      self.ftp.quit()


  def help(self):
    Msg.help()


  def jump(self):
    jumpTo = getSingleActionParam(Act["Jump"], self.action)
    if jumpTo == envs["Local"]:
      self.env = envs["Local"]
    else:
      self.pingServer(message=False)
      if self.connected:
        self.env = envs["Remote"]
      else:
        Msg.error(Ns.jump["not_connected"])


  def ls(self):
    if self.env == envs["Remote"]:
      self.pingServer()
      if self.connected:
        try:
          self.ftp.retrlines("LIST")
        except:
          Msg.error(Ns.ls["error"])
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
        Msg.error(Ns.ls["error"])


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
      Msg.error(Ns.mkdir["error"].format(dirName=dirName))


  def rush(self):
    hostStr = getSingleActionParam(Act["Rush"], self.action)
    loginStr = Ns.rush["login"]["user"]
    passwdStr = Ns.rush["login"]["passwd"]
    portSrt = Ns.rush["login"]["port"]
    userInput = Interact.multiInput([loginStr, passwdStr, portSrt])
    self.loginData = {
      "host": hostStr,
      "user": userInput[loginStr],
      "passwd": userInput[passwdStr],
      "port": userInput[portSrt] or settings["port"]
    }
    Msg.suspend(Ns.rush["connecting"].format(host=self.loginData["host"]))
    if self.login():
      Msg.success(Ns.rush["connected"].format(host=self.loginData["host"]))
    else:
      Msg.error(Ns.rush["connecting_error"].format(host=self.loginData["host"]))


  def take(self):
    self.pingServer(message=False)
    if self.connected:
      Msg.suspend(Ns.common["processing"])
      override = False
      pathExists = False
      target = getSingleActionParam(Act["Take"], self.action)
      targetPath = getNextPath(self.pathRemote, target)
      _, targetName = os.path.split(targetPath)
      localTargetPath = getNextPath(self.pathLocal, targetName)
      if os.path.exists(localTargetPath):
        pathExists = True
        confirmOverride = Interact.confirm(Ns.take["exists"].format(target=targetName))
        if confirmOverride:
          override = True
      try:
        Msg.suspend(Ns.take["progress"])
        if self.ftp.isDir(targetPath):
          currentLocalPath = self.pathLocal
          self.downloadTree(targetPath, pathExists, override)
          self.changeLocalPath(currentLocalPath)
        else:
          self.downloadFile(targetPath, pathExists, override)
        Msg.success(Ns.take["success"])
      except:
        Msg.error(Ns.take["transfer_error"])
    else:
      Msg.error(Ns.take["not_connected"])


  def whereAmI(self):
    if self.env == envs["Local"]:
      print(self.pathLocal)
    else:
      self.pingServer()
      if self.connected:
        print(self.pathRemote)


  def whoAmI(self):
    if self.env == envs["Local"]:
      print(execCmd("whoami"))
    else:
      self.pingServer()
      if self.connected:
        print(self.loginData["user"])


  def status(self):
    try:
      self.ftp.voidcmd("NOOP")
      Msg.serverResponse(self.ftp.getwelcome())
      Msg.success(Ns.status["connected_title"])
      Msg.default(Ns.status["connected_data"].format(
        host=self.loginData["host"],
        user=self.loginData["user"],
        passwd=self.loginData["passwd"],
        port=self.loginData["port"]
      ))
    except:
      Msg.error(Ns.status["disconnected_title"])
      self.setStatusDisconnected()


  #------------- Run -------------#


  def run(self):
    self.clear()
    Msg.welcome()
    while True:
      try:
        inputPrompt = getInputPrompt(self.env)
        action = input(inputPrompt)
        self.action = self.processAction(action)
        if Av.isExit(self.action):
          self.exit()
          break
        elif Av.isClear(self.action):
          self.clear()
        elif Av.isHelp(self.action):
          self.help()
        elif Av.isRush(self.action):
          self.rush()
        elif Av.isLs(self.action):
          self.ls()
        elif Av.isJump(self.action):
          self.jump()
        elif Av.isWhereAmI(self.action):
          self.whereAmI()
        elif Av.isWhoAmI(self.action):
          self.whoAmI()
        elif Av.isCd(self.action):
          self.cd()
        elif Av.isMkdir(self.action):
          self.mkdir()
        elif Av.isDelete(self.action):
          self.delete()
        elif Av.isPut(self.action):
          self.put()
        elif Av.isTake(self.action):
          self.take()
        elif Av.isStatus(self.action):
          self.status()
        else:
          Msg.info(Ns.common["command_not_found"])
      except:
        Msg.error(Ns.common["unexpected_error"])
        break
