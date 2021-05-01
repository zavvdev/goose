from halo import Halo

# Name: Spinner
# Desc: Provide interface for using terminal spinner
# Methods: 
#   - start (start spinner)
#   - success (stop with success icon)
#   - fail (stop with fail icon)
#   - stop (stop spinning)

class Spinner:
  def __init__(self):
    self.spinner = Halo(spinner="dots")

  # Name: start
  # Desc: Start spinner
  # Args: text (string)
  # Return: void

  def start(self, text):
    self.spinner.start(text)

  # ----------------------------------------------------

  # Name: success
  # Desc: Stop with success icon
  # Args: text (string)
  # Return: void

  def success(self, text):
    self.spinner.succeed(text)

  # ----------------------------------------------------

  # Name: fail
  # Desc: Stop with fail icon
  # Args: text (string)
  # Return: void

  def fail(self, text):
    self.spinner.fail(text)

  # ----------------------------------------------------

  # Name: stop
  # Desc: Stop spinner
  # Args: void
  # Return: void

  def stop(self):
    self.spinner.stop()

  # ----------------------------------------------------
