from utils.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from modules.Namespace import Namespace

Ns = Namespace()

def getInputPrompt(env):
  isRemote = env == envs["Remote"]
  previewEnv = Ns.common["envs"]["remote"] if isRemote else Ns.common["envs"]["local"]
  style = textStyles["Cyan"] + textStyles["Bold"]
  return styledText(style + Ns.common["input"].format(env=previewEnv))
  pass