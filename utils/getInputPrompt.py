from utils.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from modules.Namespace import Namespace

ns = Namespace()

def getInputPrompt(env):
  isRemote = env == envs["Remote"]
  previewEnv = ns.common["envs"]["remote"] if isRemote else ns.common["envs"]["local"]
  style = textStyles["Cyan"] + textStyles["Bold"]
  return styledText(style + ns.common["input"].format(env=previewEnv))