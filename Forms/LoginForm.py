import npyscreen as nps
from ftplib import FTP
from constants.settings import testFtp
from constants.formAccessors import formAccessors
from utils.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors
from utils.writeToFile import writeToFile
from utils.delFile import delFile
from utils.readFromFile import readFromFile
import time

ns = getNamespace(nsAccessors["Login"])

class LoginButon(nps.ButtonPress):
  def whenPressed(self):
    host = self.parent.host.value
    user = self.parent.username.value
    passwd = self.parent.passwd.value
    try:
      nps.notify_wait(ns["messages"]["connecting"])
      ftp = FTP(host)
      ftp.login(user=user, passwd=passwd)
      # data = ftp.retrlines('LIST')
      
      login_data = {
        "host": host,
        "username": user,
        "password": passwd,
      }
      writeToFile(login_data, "data/login_data.json")

      self.parent.parentApp.change_form(formAccessors["Workspace"]) 
    except:
      delFile("data/login_data.json")
      nps.notify_confirm(ns["messages"]["error"], editw=1)

class ExitButton(nps.ButtonPress):
  def whenPressed(self):
    delFile("data/login_data.json")
    self.parent.parentApp.switchForm(None)

class LoginForm(nps.FormBaseNew):
  def create(self):
    self.add(nps.FixedText, value = ns["title"])
    self.nextrely += 1
    self.host = self.add(nps.TitleText, name = ns["labels"]["host"], value = testFtp["host"])
    self.username = self.add(nps.TitleText, name = ns["labels"]["user"], value = testFtp["user"])
    self.passwd = self.add(nps.TitleText, name = ns["labels"]["passwd"], value = testFtp["passwd"])
    self.loginBtn = self.add(LoginButon, name = ns["buttons"]["login"])
    self.exitBtn = self.add(ExitButton, name = ns["buttons"]["exit"])
