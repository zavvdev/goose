from helpers.styledText import styledText
from constants.textStyles import textStyles

def getErrorMsg(msg):
  return styledText(textStyles["Red"] + msg)