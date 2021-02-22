import npyscreen as nps
from Forms.LoginForm import LoginForm
from Forms.WorkspaceForm import WorkspaceForm
from Forms.MainForm import MainForm
from constants.formAccessors import formAccessors
from constants.settings import appName
from utils.writeToFile import writeToFile

class App(nps.NPSAppManaged):
  def onStart(self):
    self.addForm(formAccessors["Main"], MainForm, name = appName)
    # self.addForm(formAccessors["Main"], LoginForm, name = appName)

  def change_form(self, name):
    self.switchForm(name)
    self.resetHistory()

if __name__ == '__main__':
  login = LoginForm()
  login.printGreeting()
  loginData = login.getLoginData()

  if writeToFile(loginData, "data/login_data.json"):  
    app = App()
    app.run()