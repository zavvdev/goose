import os
import shutil
from ftpretty import ftpretty as FTP
from constants.textStyles import textStyles
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
from helpers.getUserInput import getUserInput
from helpers.trimSpaces import trimSpaces
from helpers.getSingleActionParam import getSingleActionParam

commonNS = getNamespace(nsAccessors["Common"])
helpNS = getNamespace(nsAccessors["Help"])
rushNS = getNamespace(nsAccessors["Rush"])
jumpNS = getNamespace(nsAccessors["Jump"])
cdNS = getNamespace(nsAccessors["Cd"])
mkdirNS = getNamespace(nsAccessors["Mkdir"])
deleteNS = getNamespace(nsAccessors["Delete"])
dropNS = getNamespace(nsAccessors["Drop"])


class Goose:
  def __init__(self):
    self.ftp = None
    self.connected = False
    self.loginData = {}
    self.action = ""
    self.env = envs["Local"]
    self.pathLocal = "/"
    self.pathRemote = ""


  #------------- Utils -------------#


  def login(self):
    d = self.loginData
    try:
      self.ftp = FTP(d["h"], d["u"], d["p"])
      self.ftp.login(user=d["u"], passwd=d["p"])
      self.connected = True
      self.env = envs["Remote"]
      self.pathRemote = self.ftp.pwd()
      return True
    except:
      return False
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
    localTargetPath = getNextPath(self.pathLocal, target)
    if os.path.isfile(localTargetPath):
      confirmMsg = deleteNS["delete_file"].format(fileName=target)
      confirmDelFile = getUserConfirm(confirmMsg)
      if confirmDelFile:
        os.remove(localTargetPath)
    elif os.path.isdir(localTargetPath):
      confirmMsg = deleteNS["delete_dir"].format(dirName=target)
      confirmDelDir = getUserConfirm(confirmMsg)
      if confirmDelDir:
        shutil.rmtree(localTargetPath)
    else:
      print(getErrorMsg(deleteNS["error"].format(target=target)))
    pass


  def deleteRemote(self, target):
    remoteTargetPath = getNextPath(self.pathRemote, target)
    if isFtpDir(remoteTargetPath, self.ftp):
      confirmMsg = deleteNS["delete_dir"].format(dirName=target)
      confirmDelDir = getUserConfirm(confirmMsg)
      if confirmDelDir:
        self.rmFtpTree(remoteTargetPath)
    else:
      confirmMsg = deleteNS["delete_file"].format(fileName=target)
      confirmDelFile = getUserConfirm(confirmMsg)
      if confirmDelFile:
        self.ftp.delete(remoteTargetPath)
    pass


  def uploadFile(self, targetPath):
    self.ftp.put(targetPath, "/")
    pass


  def uploadTree(self, targetPath):
    _, dirName = os.path.split(targetPath)
    remoteDirName = getNextPath("/", dirName)
    self.ftp.upload_tree(targetPath, remoteDirName)
    pass


  #------------- Actions -------------#


  def cd(self):
    dest = getSingleActionParam(Act["Cd"], self.action)
    if self.env == envs["Local"]:
      nextLocalPath = getNextPath(self.pathLocal, dest)
      if os.path.exists(nextLocalPath):
        os.chdir(nextLocalPath)
        self.pathLocal = nextLocalPath  
      else:
        print(getErrorMsg(cdNS["error"].format(dest=nextLocalPath)))
    else:
      try:
        nextRemotePath = getNextPath(self.pathRemote, dest)
        self.ftp.cwd(nextRemotePath)
        self.pathRemote = nextRemotePath 
      except:
        print(getErrorMsg(cdNS["error"].format(dest=nextRemotePath)))
    pass


  def clear(self):
    print(execCmd("clear"))
    pass


  def delete(self):
    target = getSingleActionParam(Act["Delete"], self.action)
    try:
      if self.env == envs["Local"]:
        self.deleteLocal(target)
      else:
        self.deleteRemote(target)
    except:
      print(getErrorMsg(deleteNS["error"].format(target=target)))     
    pass


  def drop(self):
    if self.connected:
      target = getSingleActionParam(Act["Drop"], self.action)
      targetPath = getNextPath(self.pathLocal, target)
      if os.path.exists(targetPath):
        try:
          print(getSuspendMsg(dropNS["progress"]))
          if os.path.isfile(targetPath):
            self.uploadFile(targetPath)
          elif os.path.isdir(targetPath):
            self.uploadTree(targetPath)
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
    try:
      self.ftp.quit()
    except:
      pass


  def help(self):
    print(helpNS["help"])
    pass


  def jump(self):
    jumpTo = getSingleActionParam(Act["Jump"], self.action)
    if jumpTo == envs["Local"]:
      self.env = envs["Local"]
    else:
      if self.connected:
        self.env = envs["Remote"]
      else:
        print(getErrorMsg(jumpNS["not_connected"])) 
    pass


  def ls(self):
    if self.env == envs["Remote"] and self.connected:
      self.ftp.retrlines("LIST")
    else:
      if os.path.exists(self.pathLocal):
        os.chdir(self.pathLocal)
        cmd = "ls -al"
        output = execCmd(cmd)
        print(output)
      else:
        raise Exception("ls: Path not found")
    pass


  def mkdir(self):
    dirName = getSingleActionParam(Act["Mkdir"], self.action)
    try:
      if self.env == envs["Local"]:
        localDirPath = getNextPath(self.pathLocal, dirName)
        os.mkdir(localDirPath)
      else:
        remoteDirPath = getNextPath(self.pathRemote, dirName)
        self.ftp.mkd(remoteDirPath)
    except:
      print(getErrorMsg(mkdirNS["error"].format(dirName=dirName)))
    pass


  def rush(self):
    hostStr = getSingleActionParam(Act["Rush"], self.action)
    loginStr = rushNS["login"]["u"]
    passwdStr = rushNS["login"]["p"]
    userInput = getUserInput([loginStr, passwdStr])
    self.loginData = {
      "h": "192.168.0.105", #hostStr,
      "u": "ubuntu-ftp", #userInput[loginStr],
      "p": "123", #userInput[passwdStr]
    }
    msg = getSuspendMsg(rushNS["connecting"].format(host=self.loginData["h"]))
    print(msg)
    if self.login():
      msg = rushNS["connected"].format(host=self.loginData["h"])
      print(getSuccessMsg(msg))
    else:
      print(getErrorMsg(rushNS["connecting_error"]))
    pass


  def whereAmI(self):
    if self.env == envs["Local"]:
      print(self.pathLocal)
    else:
      print(self.pathRemote)
    pass


  def whoAmI(self):
    if self.env == envs["Local"]:
      print(execCmd("whoami"))
    else:
      print(self.loginData["u"])
    pass


  #------------- Run -------------#


  def run(self):
    print(styledText(textStyles["Bold"] + commonNS["app_name"]))
    while True:
      try:
        isRemote = self.env == envs["Remote"]
        env = commonNS["envs"]["remote"] if isRemote else commonNS["envs"]["local"]
        style = textStyles["Cyan"] + textStyles["Bold"]
        inputText = styledText(
          style + commonNS["input"].format(env=env)
        )
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
        else:
          print(getInfoMsg(commonNS["not_found"]))
      except:
        print(getErrorMsg(commonNS["unexpected_error"]))
    pass
