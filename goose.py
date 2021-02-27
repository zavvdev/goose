from ftplib import FTP
from constants.settings import ColorPalette as C
from helpers.ActionVerificators.isExit import isExit
from helpers.ActionVerificators.isHelp import isHelp
from helpers.ActionVerificators.isRush import isRush
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

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
    print(C.VIOLET + msg + C.ENDC)

    if l == 2:
      self.loginData = { "h": s[1], "u": "", "p": ""}
    elif l == 4:
      self.loginData = { "h": s[1], "u": s[3], "p": "" }
    else:
      self.loginData = { "h": s[1], "u": s[3], "p": s[5] }

    if self.login():
      msg = rushNS["connected"].format(host=self.loginData["h"])
      print(C.GREEN + msg + C.ENDC)
      self.ftp.retrlines("LIST") 
    else:
      errorMsg = rushNS["connecting_error"]
      print(C.RED + errorMsg + C.ENDC)
    pass

  def run(self):
    print(C.BOLD + commonNS["app_name"] + C.ENDC)

    while True:
      self.action = input(C.CYAN + C.BOLD + commonNS["input"] + C.ENDC)

      if isExit(self.action):
        break
      elif isHelp(self.action):
        self.help()
      elif isRush(self.action):
        self.rush()
      else:
        print(C.YELLOW + commonNS["not_found"] + C.ENDC)
    pass

goose = Goose()
goose.run()


  