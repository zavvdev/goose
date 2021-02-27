from ftplib import FTP
from constants.textStyles import textStyles
from helpers.ActionVerificators.isExit import isExit
from helpers.ActionVerificators.isHelp import isHelp
from helpers.ActionVerificators.isRush import isRush
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors
from helpers.styledText import styledText
from constants.textStyles import textStyles

commonNS = getNamespace(nsAccessors["Common"])
helpNS = getNamespace(nsAccessors["Help"])
rushNS = getNamespace(nsAccessors["Rush"])

class Goose:
  def __init__(self):
    ftp = None
    loginData = {}
    action = ""

  def login(self):
    d = self.loginData
    try:
      self.ftp = FTP(d["h"])
      self.ftp.login(user=d["u"], passwd=d["p"])
      return True
    except:
      return False
    pass

  def help(self):
    print(helpNS["help"])
    pass

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

  def run(self):
    print(styledText(textStyles["Bold"] + commonNS["app_name"]))

    while True:
      inputText = styledText(
        textStyles["Cyan"] + textStyles["Bold"] + commonNS["input"]
      )
      self.action = input(inputText)

      if isExit(self.action):
        break
      elif isHelp(self.action):
        self.help()
      elif isRush(self.action):
        self.rush()
      else:
        print(styledText(textStyles["Yellow"] + commonNS["not_found"]))
    pass

goose = Goose()
goose.run()


  