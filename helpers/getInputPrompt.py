from helpers.styledText import styledText
from constants.textStyles import textStyles

def getInputPrompt(text):
  style = textStyles["Cyan"] + textStyles["Bold"]
  return styledText(style + text)
  pass