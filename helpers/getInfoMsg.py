from helpers.styledText import styledText
from constants.textStyles import textStyles

def getInfoMsg(msg):
  return styledText(textStyles["Yellow"] + msg)