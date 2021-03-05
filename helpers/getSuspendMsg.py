from helpers.styledText import styledText
from constants.textStyles import textStyles

def getSuspendMsg(msg):
  return styledText(textStyles["Violet"] + msg)