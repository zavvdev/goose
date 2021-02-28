from constants.actions import Actions as Act
from helpers.styledText import styledText
from constants.textStyles import textStyles
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

commonNS = getNamespace(nsAccessors["Common"])

def getUserConfirm(question):
  q = question + "\n"
  yesAct = Act["Confirm"]["Yes"]
  yesShortAct = Act["Confirm"]["YesShort"]
  confTip = commonNS["confirm"]["tip"]
  conf = input(styledText(textStyles["Yellow"] + q + confTip))

  if conf.lower() == yesAct or conf.lower() == yesShortAct:
    return True
  else:
    return False

  pass