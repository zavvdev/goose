from utils.styledText import styledText
from constants.textStyles import textStyles
from constants.environments import environments as envs
from modules.Namespace import Namespace

ns = Namespace()

# Name: getInputPrompt
# Desc: Get styled application input prompt
# Args: env (string<Key of environmets>)
# Return: string

def getInputPrompt(env):
  isRemote = env == envs["Remote"]
  remotePreview = ns.common["prompt_env"]["remote"]
  localPreview = ns.common["prompt_env"]["local"]
  previewEnv = remotePreview if isRemote else localPreview
  style = textStyles["Cyan"] + textStyles["Bold"]
  return styledText(style + ns.common["input"].format(env=previewEnv))

# ----------------------------------------------------