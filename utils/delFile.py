import os

def delFile(pathToFile):
  try:
    os.remove(pathToFile)
    return True
  except:
    return False