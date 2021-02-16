import npyscreen as nps
from Boxes.LoginBox import LoginBox

class MainForm(nps.FormBaseNew):
  def create(self):
    y, x = self.useable_space()

    self.LoginBox = self.add(LoginBox, name = "Connect", value = 0, relx = 4, max_width = -1, rely = 2, max_height = y // 5)
    pass
