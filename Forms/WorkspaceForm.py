import npyscreen as nps
from utils.readFromFile import readFromFile

class WorkspaceForm(nps.ActionForm):
  def create(self):    
    login_data = readFromFile("data/login_data.json")
    if login_data:
      self.add(nps.FixedText, value = str(login_data))

  def on_ok(self):
    self.parentApp.switchForm(None)
    pass

  def on_cancel(self):
    self.parentApp.switchForm(None)
    pass