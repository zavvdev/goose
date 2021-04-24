from constants.actions import Actions as Act
from helpers.styledText import styledText
from constants.textStyles import textStyles
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

commonNS = getNamespace(nsAccessors["Common"])

class Interact:
  def __init__(self):
    pass

  def confirm(self, question):
    q = question + "\n"
    yesAct = Act["Confirm"]["Yes"]
    yesShortAct = Act["Confirm"]["YesShort"]
    confTip = commonNS["confirm"]["tip"]
    conf = input(styledText(textStyles["Yellow"] + q + confTip))
    confLover = conf.lower()
    if confLover == yesAct or confLover == yesShortAct:
      return True
    return False
    pass

  def multiInput(self, fields):
    result = {}
    for field in fields:
      userInput = input(field + ": ")
      result[field] = userInput
    return result
    pass