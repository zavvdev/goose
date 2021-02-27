from ftplib import FTP
from constants.textStyles import textStyles
from helpers.ActionVerificators.isExit import isExit
from helpers.ActionVerificators.isHelp import isHelp
from helpers.ActionVerificators.isRush import isRush
from helpers.ActionVerificators.isLs import isLs
from helpers.ActionVerificators.isJump import isJump
from helpers.ActionVerificators.isClear import isClear
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors
from helpers.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from constants.actions import Actions as Act
from helpers.execCmd import execCmd

commonNS = getNamespace(nsAccessors["Common"])
helpNS = getNamespace(nsAccessors["Help"])
rushNS = getNamespace(nsAccessors["Rush"])
jumpNS = getNamespace(nsAccessors["Jump"])

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
      self.ftp = FTP(d["h"])
      self.ftp.login(user=d["u"], passwd=d["p"])
      self.connected = True
      self.env = envs["Remote"]
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
      print(styledText(textStyles["Green"] + msg))
    else:
      errorMsg = rushNS["connecting_error"]
      print(styledText(textStyles["Red"] + errorMsg))
    pass

  #-----------------------------------

  def ls(self):
    if self.env == envs["Remote"]:
      self.ftp.retrlines("LIST")
    else:
      cmd = "cd {path}; ls -al".format(path=self.pathLocal)
      output = execCmd(cmd)
      print(output)
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
        print(styledText(textStyles["Red"] + jumpNS["not_connected"]))
    pass

  #-----------------------------------

  def clear(self):
    print(execCmd("clear"))
    pass


  #------------- Run -------------#


  def run(self):
    print(styledText(textStyles["Bold"] + commonNS["app_name"]))

    while True:
      env = commonNS["envs"]["remote"] if self.env == envs["Remote"] else commonNS["envs"]["local"]
      inputText = styledText(
        textStyles["Cyan"] + textStyles["Bold"] + commonNS["input"].format(env=env)
      )
      self.action = input(inputText)

      if isExit(self.action):
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
      else:
        print(styledText(textStyles["Yellow"] + commonNS["not_found"]))
    pass
