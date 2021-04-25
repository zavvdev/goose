from utils.styledText import styledText
from constants.textStyles import textStyles
from modules.Namespace import Namespace

ns = Namespace().interact

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
    yes = ns["confirm"]["yes"]
    yesShort = ns["confirm"]["short_yes"]
    confTip = ns["confirm"]["tip"]
    conf = input(styledText(textStyles["Yellow"] + q + confTip))
    confLover = conf.lower()
    if confLover == yes or confLover == yesShort:
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