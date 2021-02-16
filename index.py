import npyscreen as nps
from Forms.LoginForm import LoginForm
from Forms.WorkspaceForm import WorkspaceForm
from constants.formAccessors import formAccessors
from constants.settings import appName
from utils.writeToFile import writeToFile

class App(nps.NPSAppManaged):
  def onStart(self):
    self.addForm(formAccessors["Main"], WorkspaceForm, name = appName)
    # self.addForm(formAccessors["Main"], LoginForm, name = appName)

  def change_form(self, name):
    self.switchForm(name)
    self.resetHistory()

if __name__ == '__main__':
  host = input("Host: ")
  user = input("Username: ")
  passwd = input("Password: ")

  login_data = {
    "host": host,
    "username": user,
    "password": passwd,
  }
  writeToFile(login_data, "data/login_data.json")
  app = App()
  app.run()