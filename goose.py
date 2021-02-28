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

commonNS = getNamespace(nsAccessors["Common"])
helpNS = getNamespace(nsAccessors["Help"])
rushNS = getNamespace(nsAccessors["Rush"])
jumpNS = getNamespace(nsAccessors["Jump"])
cdNS = getNamespace(nsAccessors["Cd"])
mkdirNS = getNamespace(nsAccessors["Mkdir"])
deleteNS = getNamespace(nsAccessors["Delete"])

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
      self.connected = True
      self.env = envs["Remote"]
      self.pathRemote = self.ftp.pwd()
      return True
    except:
      return False
    pass


  #------------- Actions -------------#


  def help(self):
    print(helpNS["help"])
    pass

  #-----------------------------------

  def rush(self):
    i = self.action
    s = i.split(" ")
    l = len(s)

    msg = rushNS["connecting"].format(host=s[1])
    print(styledText(textStyles["Violet"] + msg))

    if l == 2:
      self.loginData = { "h": s[1], "u": "", "p": ""}
    elif l == 4:
      self.loginData = { "h": s[1], "u": s[3], "p": "" }
    else:
      self.loginData = { "h": s[1], "u": s[3], "p": s[5] }

    if self.login():
      msg = rushNS["connected"].format(host=self.loginData["h"])
      print(getSuccessMsg(msg))
    else:
      print(getErrorMsg(rushNS["connecting_error"]))
    pass

  #-----------------------------------

  def ls(self):
    if self.env == envs["Remote"]:
      self.ftp.retrlines("LIST")
    else:
      if os.path.exists(self.pathLocal):
        cmd = "cd {path}; ls -al".format(path=self.pathLocal)
        output = execCmd(cmd)
        print(output)
      else:
        raise Exception("ls: Path not found")
    pass

  #-----------------------------------

  def jump(self):
    jumpTo = self.action.split(" ")[1]

    if jumpTo == Act["Jump"]["local"]:
      self.env = envs["Local"]
    else:
      if self.connected:
        self.env = envs["Remote"]
      else:
        print(getErrorMsg(jumpNS["not_connected"]))
    pass

  #-----------------------------------

  def clear(self):
    print(execCmd("clear"))
    pass

  #-----------------------------------

  def whereAmI(self):
    if self.env == envs["Local"]:
      print(self.pathLocal)
    else:
      print(self.pathRemote)

  #-----------------------------------

  def whoAmI(self):
    if self.env == envs["Local"]:
      print(execCmd("whoami"))
    else:
      print(self.loginData["u"])

  #-----------------------------------

  def exit(self):
    try:
      self.ftp.quit()
    except:
      pass

  #-----------------------------------

  def cd(self):
    dest = self.action.split(" ")[1]

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

  #-----------------------------------

  def mkdir(self):
    dirName = self.action.split(" ")[1]

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

  #-----------------------------------

  def delete(self):
    target = self.action.split(" ")[1]

    try:
      if self.env == envs["Local"]:
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
      else:
        remoteTargetPath = getNextPath(self.pathRemote, target)
        confirmMsg = deleteNS["delete_dir"].format(dirName=target)
        confirmDelDir = getUserConfirm(confirmMsg)
        if confirmDelDir:
          self.ftp.rmd(remoteTargetPath)
    except:
      print(getErrorMsg(deleteNS["error"].format(target=target)))
            
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
        else:
          print(getInfoMsg(commonNS["not_found"]))
      except:
        print(getErrorMsg(commonNS["unexpected_error"]))
    pass
