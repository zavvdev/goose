import os
import shutil
from pathlib import Path

from modules.ActionVerifier import ActionVerifier
from modules.Message import Message
from modules.Ftp import Ftp
from modules.Interact import Interact
from modules.Namespace import Namespace
from modules.Spinner import Spinner

from constants.settings import settings
from constants.environments import environments as envs
from constants.actions import actions as act

from utils.execCmd import execCmd
from utils.getNextPath import getNextPath
from utils.trimSpaces import trimSpaces
from utils.getSingleActionParam import getSingleActionParam
from utils.getInputPrompt import getInputPrompt

av = ActionVerifier()
msg = Message()
interact = Interact()
ns = Namespace()
spinner = Spinner()

class App:
  def __init__(self):
    self.ftp = None
    self.connected = False
    self.loginData = {}
    self.action = ""
    self.env = envs["Local"]
    self.pathLocal = str(Path.home())
    self.pathRemote = ""


  # # # # # # # # # # # #
  #                     #
  #        Utils        #
  #                     #
  # # # # # # # # # # # #


  # Name: processAction
  # Desc: Process user input
  # Args: action (string)
  # Return: String with only single spaces

  def processAction(self, action):
    return trimSpaces(action)

  # ----------------------------------------------------

  # Name: pingServer
  # Desc: Check connection status
  # Args: message (boolean)
  # Return: void

  def pingServer(self, message=True):
    try:
      self.ftp.voidcmd("NOOP")
    except:
      if message:
        msg.error(ns.errors["no_connection"])
      self.setStatusDisconnected()

  # ----------------------------------------------------

  # Name: setStatusDisconnected
  # Desc: Set application status to disconnected state
  # Args: void
  # Return: void

  def setStatusDisconnected(self):
    self.ftp = None
    self.connected = False
    self.env = envs["Local"]
    self.pathRemote = ""

  # ----------------------------------------------------

  # Name: login
  # Desc: Establish connection with remote ftp-server
  # Args: void
  # Return: boolean

  def login(self):
    loginData = self.loginData
    try:
      self.ftp = Ftp(
        loginData["host"],
        loginData["user"],
        loginData["passwd"],
        port=loginData["port"],
        timeout=settings["ftp"]["timeout"]
      )
      self.ftp.login(user=loginData["user"], passwd=loginData["passwd"])
      self.connected = True
      self.env = envs["Remote"]
      self.pathRemote = self.ftp.pwd()
      return True
    except Exception as e:
      raise e

  # ----------------------------------------------------

  # Name: changeLocalPath
  # Desc: Change local file system path 
  # Args: nextPath (string)
  # Return: void

  def changeLocalPath(self, nextPath):
    os.chdir(nextPath)
    self.pathLocal = nextPath

  # ----------------------------------------------------

  # Name: changeRemotePath
  # Desc: Change remote file system path 
  # Args: nextPath (string)
  # Return: void

  def changeRemotePath(self, nextPath):
    self.ftp.cwd(nextPath)
    self.pathRemote = nextPath 

  # ----------------------------------------------------

  
  # # # # # # # # # # # # #
  #                       #
  #        Actions        #
  #                       #
  # # # # # # # # # # # # #


  # Name: connect
  # Desc: Connect to remote ftp-server
  # Args: void
  # Return: void

  def connect(self):
    hostStr = getSingleActionParam(act["Connect"], self.action)
    loginStr = ns.common["login"]["user"]
    passwdStr = ns.common["login"]["passwd"]
    portSrt = ns.common["login"]["port"]
    userInput = interact.multiInput([loginStr, passwdStr, portSrt])
    self.loginData = {
      "host": hostStr,
      "user": userInput[loginStr],
      "passwd": userInput[passwdStr],
      "port": userInput[portSrt] or settings["ftp"]["port"]
    }
    connectingMsg = ns.common["connecting"].format(host=self.loginData["host"])
    connectedMsg = ns.common["connected"].format(host=self.loginData["host"])
    errorMsg = ns.errors["connecting_error"].format(host=self.loginData["host"])
    spinner.start(connectingMsg)
    try:
      isConnected = self.login()
      if isConnected:
        spinner.success(connectingMsg)
        msg.default(self.ftp.getwelcome())
        msg.success(connectedMsg)
    except Exception as e:
      spinner.fail(connectingMsg)
      self.setStatusDisconnected()
      msg.default(e)
      msg.error(errorMsg)

  # ----------------------------------------------------

  # Name: upload
  # Desc: Upload data to remote ftp-server
  # Args: void
  # Return: void

  def upload(self):
    self.pingServer(message=False)
    if self.connected:
      overwrite = False
      pathExists = False
      target = getSingleActionParam(act["Upload"], self.action)
      targetPath = getNextPath(self.pathLocal, target)
      _, targetName = os.path.split(target)
      if os.path.exists(targetPath):
        if self.ftp.exists(targetName, self.pathRemote):
          pathExists = True
          existsMsg = ns.interact["data_exists"].format(target=targetName)
          confirmOverwrite = interact.confirm(existsMsg)
          if confirmOverwrite:
            overwrite = True
        uploadingMsg = ns.common["uploading"].format(target=targetPath)
        try:
          spinner.start(uploadingMsg)
          if os.path.isdir(targetPath):
            self.ftp.putTree(targetPath, pathExists, overwrite)
          else:
            self.ftp.putFile(targetPath, pathExists, overwrite)
          spinner.success(uploadingMsg)
          msg.success(ns.common["success"])
        except Exception as e:
          spinner.fail(uploadingMsg)
          msg.default(e)
          msg.error(ns.errors["transfer_error"])
      else:
        msg.error(ns.errors["invalid_path"])
    else:
      msg.error(ns.errors["no_connection"])

  # ----------------------------------------------------

  # Name: download
  # Desc: Download data from remote ftp-server
  # Args: void
  # Return: void

  def download(self):
    self.pingServer(message=False)
    if self.connected:
      overwrite = False
      pathExists = False
      target = getSingleActionParam(act["Download"], self.action)
      targetPath = getNextPath(self.pathRemote, target)
      _, targetName = os.path.split(targetPath)
      localTargetPath = getNextPath(self.pathLocal, targetName)
      if os.path.exists(localTargetPath):
        pathExists = True
        confirmOverwrite = interact.confirm(ns.interact["data_exists"].format(target=targetName))
        if confirmOverwrite:
          overwrite = True
      downloadingMsg = ns.common["downloading"].format(target=targetPath)
      try:
        spinner.start(downloadingMsg)
        if self.ftp.isDir(targetPath):
          self.ftp.getTree(targetPath, pathExists, overwrite)
        else:
          self.ftp.getFile(targetPath, self.pathLocal, pathExists, overwrite)
        spinner.success(downloadingMsg)
        msg.success(ns.common["success"])
      except Exception as e:
        spinner.fail(downloadingMsg)
        msg.default(e)
        msg.error(ns.errors["transfer_error"])
    else:
      msg.error(ns.errors["no_connection"])

  # ----------------------------------------------------

  # Name: delete
  # Desc: Delete local or remote file/directory
  # Args: void
  # Return: void

  def delete(self):
    target = getSingleActionParam(act["Delete"], self.action)
    _, targetName = os.path.split(target)
    deletingMsg = ns.common["deleting"].format(target=target)
    confirmMsg = ns.interact["confirm_delete"].format(fileName=targetName)
    confirmDel = interact.confirm(confirmMsg)
    if confirmDel:
      spinner.start(deletingMsg)
      try:
        _, targetName = os.path.split(target)
        if self.env == envs["Local"]:
          localTargetPath = getNextPath(self.pathLocal, targetName)      
          if os.path.isdir(localTargetPath):
            shutil.rmtree(localTargetPath)
          else:
            os.remove(localTargetPath)
        else:
          self.pingServer()
          if self.connected:
            remoteTargetPath = getNextPath(self.pathRemote, targetName)
            if self.ftp.isDir(remoteTargetPath):
              self.ftp.rmTree(remoteTargetPath)
            else:
              self.ftp.delete(remoteTargetPath)
        spinner.success(deletingMsg)
        msg.success(ns.common["success"])
      except Exception as e:
        spinner.fail(deletingMsg)
        msg.default(e)
        msg.error(ns.errors["delete_error"].format(target=target)) 

  # ----------------------------------------------------

  # Name: mkdir
  # Desc: Create new local or remote directory
  # Args: void
  # Return: void

  def mkdir(self):
    dirName = getSingleActionParam(act["Mkdir"], self.action)
    try:
      if self.env == envs["Local"]:
        localDirPath = getNextPath(self.pathLocal, dirName)
        os.mkdir(localDirPath)
      else:
        self.pingServer()
        if self.connected:
          remoteDirPath = getNextPath(self.pathRemote, dirName)
          self.ftp.mkd(remoteDirPath)
    except Exception as e:
      msg.default(e)
      msg.error(ns.errors["mkdir_error"].format(dirName=dirName))

  # ----------------------------------------------------

  # Name: changeEnv
  # Desc: Change current working environment
  # Args: void
  # Return: void

  def changeEnv(self):
    changeTo = getSingleActionParam(act["ChangeEnv"], self.action)
    if changeTo == envs["Local"]:
      self.env = envs["Local"]
    else:
      self.pingServer()
      if self.connected:
        self.env = envs["Remote"]
      
  # ----------------------------------------------------

  # Name: cd
  # Desc: Change local/remote directory
  # Args: void
  # Return: void

  def cd(self):
    dest = getSingleActionParam(act["Cd"], self.action)
    if self.env == envs["Local"]:
      nextLocalPath = getNextPath(self.pathLocal, dest)
      if os.path.exists(nextLocalPath):
        self.changeLocalPath(nextLocalPath)  
      else:
        msg.error(ns.errors["cd_error"].format(dest=nextLocalPath))
    else:
      self.pingServer()
      if self.connected:
        try:
          nextRemotePath = getNextPath(self.pathRemote, dest)
          self.changeRemotePath(nextRemotePath)
        except Exception as e:
          msg.default(e)
          msg.error(ns.errors["cd_error"].format(dest=nextRemotePath))

  # ----------------------------------------------------

  # Name: ls
  # Desc: Print list of data in current local/remote directory 
  # Args: void
  # Return: void

  def ls(self):
    if self.env == envs["Remote"]:
      self.pingServer()
      if self.connected:
        try:
          self.ftp.retrlines("LIST")
        except Exception as e:
          msg.default(e)
          msg.error(ns.errors["terminal_command_error"].format(command="ls"))
    else:
      try:
        if os.path.exists(self.pathLocal):
          os.chdir(self.pathLocal)
          cmd = "ls -l"
          output = execCmd(cmd)
          print(output)
        else:
          raise
      except Exception as e:
        msg.default(e)
        msg.error(ns.errors["terminal_command_error"].format(command="ls"))

  # ----------------------------------------------------

  # Name: status
  # Desc: Print status of connection
  # Args: void
  # Return: void

  def status(self):
    try:
      self.ftp.voidcmd("NOOP")
      msg.default(self.ftp.getwelcome())
      msg.success(ns.common["status"]["connected"])
      msg.default(ns.common["status"]["connected_data"].format(
        host=self.loginData["host"],
        user=self.loginData["user"],
        passwd=self.loginData["passwd"],
        port=self.loginData["port"]
      ))
    except:
      msg.error(ns.common["status"]["disconnected"])
      self.setStatusDisconnected()

  # ----------------------------------------------------

  # Name: clear
  # Desc: Clear previous terminal inputs
  # Args: void
  # Return: void

  def clear(self):
    clearResult = execCmd("clear")
    if clearResult:
      print(clearResult)
    else:
      msg.error(ns.errors["terminal_command_error"].format(command="clear"))

  # ----------------------------------------------------

  # Name: whereAmI
  # Desc: Print current local/remote file system path
  # Args: void
  # Return: void

  def whereAmI(self):
    if self.env == envs["Local"]:
      msg.default(self.pathLocal)
    else:
      self.pingServer()
      if self.connected:
        msg.default(self.pathRemote)

  # ----------------------------------------------------

  # Name: whoAmI
  # Desc: Print current local/remote username
  # Args: void
  # Return: void

  def whoAmI(self):
    if self.env == envs["Local"]:
      msg.default(execCmd("whoami"))
    else:
      self.pingServer()
      if self.connected:
        msg.default(self.loginData["user"])

  # ----------------------------------------------------

  # Name: exit
  # Desc: Terminate application
  # Args: void
  # Return: void

  def exit(self):
    self.pingServer(message=False)
    if self.connected and self.ftp:
      self.ftp.quit()

  # ----------------------------------------------------

  # Name: help
  # Desc: Print help message
  # Args: void
  # Return: void

  def help(self):
    msg.help()

  # ----------------------------------------------------

  # Name: run
  # Desc: Start application. Listen for actions
  # Args: void
  # Return: void

  def run(self):
    self.clear()
    msg.welcome()
    while True:
      try:
        inputPrompt = getInputPrompt(self.env)
        action = input(inputPrompt)
        self.action = self.processAction(action)
        if av.isExit(self.action):
          self.exit()
          break
        elif av.isClear(self.action):
          self.clear()
        elif av.isHelp(self.action):
          self.help()
        elif av.isConnect(self.action):
          self.connect()
        elif av.isLs(self.action):
          self.ls()
        elif av.isChangeEnv(self.action):
          self.changeEnv()
        elif av.isWhereAmI(self.action):
          self.whereAmI()
        elif av.isWhoAmI(self.action):
          self.whoAmI()
        elif av.isCd(self.action):
          self.cd()
        elif av.isMkdir(self.action):
          self.mkdir()
        elif av.isDelete(self.action):
          self.delete()
        elif av.isUpload(self.action):
          self.upload()
        elif av.isDownload(self.action):
          self.download()
        elif av.isStatus(self.action):
          self.status()
        else:
          msg.info(ns.common["command_not_found"])
      except:
        msg.error(ns.errors["unexpected_error"])
        break
  
  # ----------------------------------------------------
