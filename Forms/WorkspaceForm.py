import npyscreen as nps

class WorkspaceForm(nps.ActionForm):
  def create(self):    
    self.add(nps.FixedText, value = "Workspace")

  def on_ok(self):
    self.parentApp.switchForm(None)
    pass

  def on_cancel(self):
    self.parentApp.switchForm(None)
    pass