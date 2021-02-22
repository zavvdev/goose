from ftplib import FTP
from constants.settings import testFtp
from constants.formAccessors import formAccessors
from utils.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors
from utils.writeToFile import writeToFile
from utils.delFile import delFile
from utils.readFromFile import readFromFile
import time
from constants.settings import testFtp

ns = getNamespace(nsAccessors["Login"])

class LoginForm():
  def __init__(self):
    self.greetingText = ns["greeting"]
    self.titleText = ns["title"]
    self.hostLabel = ns["labels"]["host"]
    self.userLabel = ns["labels"]["user"]
    self.passwdLabel = ns["labels"]["passwd"]
    self.connectingMessage = ns["messages"]["connecting"]
    self.errorMessage = ns["messages"]["error"]

  def printGreeting(self):
    print(self.greetingText)

  def getLoginData(self):
    print(self.titleText)
    host = input(self.hostLabel)
    username = input(self.userLabel)
    passwd = input(self.passwdLabel)

    loginData = {
      "host": testFtp["host"],
      "username": testFtp["user"],
      "password": testFtp["passwd"]
    }
    
    return loginData

  