from helpers.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from helpers.getNamespace import getNamespace
from constants.nsAccessors import nsAccessors

commonNS = getNamespace(nsAccessors["Common"])

def getInputPrompt(env):
  isRemote = env == envs["Remote"]
  previewEnv = commonNS["envs"]["remote"] if isRemote else commonNS["envs"]["local"]
  style = textStyles["Cyan"] + textStyles["Bold"]
  return styledText(style + commonNS["input"].format(env=previewEnv))
  pass