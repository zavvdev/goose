from helpers.styledText import styledText
from constants.textStyles import textStyles

def getSuccessMsg(msg):
  return styledText(textStyles["Green"] + msg)