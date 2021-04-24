from helpers.styledText import styledText
from constants.textStyles import textStyles
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

commonNS = getNamespace(nsAccessors["Common"])

def getWelcome():
  welcomeMessage = commonNS["welcome_message"]
  style = textStyles["Bold"] + textStyles["White"]
  return styledText(style + welcomeMessage)
  pass