from constants.actions import Actions as Act
from utils.styledText import styledText
from constants.textStyles import textStyles
from modules.Namespace import Namespace

ns = Namespace()

# Name: Interact
# Desc: Provide opportunities for interactions with the application
# Inherits: None
# Methods: 
#   - confirm (confirm some statement)
#   - multiInput (collect multiple user responses)

class Interact:

  # Name: confirm
  # Desc: Confirm some statement
  # Args: question (string)
  # Return: boolean

  def confirm(self, question):
    q = question + "\n"
    yesAct = Act["Confirm"]["Yes"]
    yesShortAct = Act["Confirm"]["YesShort"]
    confTip = ns.common["confirm"]["tip"]
    conf = input(styledText(textStyles["Yellow"] + q + confTip))
    confLover = conf.lower()
    if confLover == yesAct or confLover == yesShortAct:
      return True
    return False

  # ----------------------------------------------------

  # Name: multiInput
  # Desc: Collect multiple user responses
  # Args: fields (Array of strings)
  # Return: Dictionary,
  #         each key - key of fields array, each value - user response 

  def multiInput(self, fields):
    result = {}
    for field in fields:
      userInput = input(field + ": ")
      result[field] = userInput
    return result

  # ----------------------------------------------------