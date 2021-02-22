import npyscreen as nps
from utils.readFromFile import readFromFile
from constants.nsAccessors import nsAccessors
from utils.getNamespace import getNamespace
from ftplib import FTP
from utils.delFile import delFile
import os
import subprocess

ns = getNamespace(nsAccessors["Login"])

def subprocess_cmd(command):
  process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
  proc_stdout = process.communicate()[0].strip()
  return proc_stdout.decode("utf-8").split("\n")

class MainForm(nps.FormBaseNew):
  def create(self):  
    y, x = self.useable_space()
    self.loginData = readFromFile("data/login_data.json")
    if self.loginData:
      try:
        nps.notify_wait(ns["messages"]["connecting"])
        self.ftp = FTP(self.loginData["host"])
        self.ftp.login(user=self.loginData["username"], passwd=self.loginData["password"])

      except:
        delFile("data/login_data.json")
        nps.notify_confirm(ns["messages"]["error"], editw=1)
        self.parentApp.switchForm(None)

      remoteList = self.ftp.nlst()
      # localList = os.listdir("/")

      # process = subprocess.run(["ls", "-al"], stdout=subprocess.PIPE)
      # localList = process.stdout.decode("utf-8").split("\n")

      localList = subprocess_cmd("cd /; ls -al")

      localListBox = self.add(nps.BoxTitle, name="Local files",
        values=localList, relx=3,
        rely=2, max_width=x // 2 - 4, max_height=-1)

      remoteListBoc = self.add(nps.BoxTitle, name="Remote files",
        values=remoteList, relx= -1 + (x // 2 + 4),
        rely=2, max_width=x // 2 - 4, max_height=-1)

      # obj = self.add(nps.BoxTitle, name="BoxTitle",
      #   values=["first line", "second line"],
      #   rely=y + y//5, max_width=-1, max_height=y // 5)

  # def on_ok(self):
  #   self.parentApp.switchForm(None)
  #   pass

  # def on_cancel(self):
  #   self.parentApp.switchForm(None)
  #   pass