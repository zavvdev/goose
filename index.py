import npyscreen as nps
from Forms.LoginForm import LoginForm
from Forms.WorkspaceForm import WorkspaceForm
from constants.formAccessors import formAccessors
from constants.settings import appName

class App(nps.NPSAppManaged):
  def onStart(self):
    self.addForm(formAccessors["Main"], LoginForm, name = appName)
    self.addForm(formAccessors["Workspace"], WorkspaceForm, name = appName)

  def change_form(self, name):
    self.switchForm(name)
    self.resetHistory()

if __name__ == '__main__':
  app = App()
  app.run()